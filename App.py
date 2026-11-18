
import os
import streamlit as st
import wikipedia

from datetime import date, timedelta
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

st.set_page_config(
    page_title="Study Buddy AI",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background-color: #101827;
    color: white;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #60A5FA;
}

.subtitle {
    text-align: center;
    color: #94A3B8;
    font-size: 17px;
}

section[data-testid="stSidebar"] {
    background-color: #172235;
}

[data-testid="stChatMessage"] {
    background-color: #1E293B;
    border-radius: 15px;
    padding: 15px;
}

.stButton button {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


load_dotenv(override=True)

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    st.error("Groq API Key not found! Check your .env file.")
    st.stop()


exam_offsets = {
    "math": 5,
    "science": 9,
    "english": 12,
    "computer science": 15
}


@tool
def get_exam_info(subject: str) -> str:
    """Get exam date and remaining days for a school subject."""

    subject = subject.strip().lower()

    if subject in exam_offsets:

        today = date.today()

        exam_date = today + timedelta(
            days=exam_offsets[subject]
        )

        days_left = (exam_date - today).days

        return (
            f"{subject.title()} exam is on "
            f"{exam_date.strftime('%A, %d %B %Y')}. "
            f"{days_left} days remaining."
        )

    return (
        f"No exam found for {subject}. "
        f"Available subjects: {', '.join(exam_offsets.keys())}"
    )


@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia for educational information."""

    try:

        results = wikipedia.search(query, results=3)

        if not results:
            return "No Wikipedia results found."

        page = wikipedia.page(
            results[0],
            auto_suggest=False
        )

        return page.summary[:3500]

    except wikipedia.exceptions.DisambiguationError as e:

        return (
            "Please make your search more specific: "
            + ", ".join(e.options[:5])
        )

    except wikipedia.exceptions.PageError:

        return "No Wikipedia page found."

    except Exception as e:

        return f"Wikipedia error: {str(e)}"


@st.cache_resource
def create_study_agent():

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        api_key=API_KEY
    )

    agent = create_agent(
        model=llm,
        tools=[
            wikipedia_search,
            get_exam_info
        ],
        system_prompt="""
        You are Study Buddy, a friendly AI assistant
        for school students.

        Your responsibilities:

        1. Explain school topics in simple language.
        2. Help students understand difficult concepts.
        3. Use Wikipedia for educational research when useful.
        4. ALWAYS use get_exam_info for exam questions.
        5. Never invent exam dates.
        6. Give clear and accurate answers.
        7. Use headings and bullet points when useful.
        8. Be friendly and encouraging.
        """
    )

    return agent


agent = create_study_agent()


if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


with st.sidebar:

    st.title("🎓 Study Buddy")

    st.write("Your Personal AI Learning Assistant")

    st.divider()

    st.subheader("📚 Features")

    st.write("💬 AI Chat")
    st.write("📅 Exam Information")
    st.write("🔍 Wikipedia Search")
    st.write("🤖 AI Agent")

    st.divider()

    st.subheader("💡 Try asking")

    examples = [
        "When is my Science exam?",
        "Explain photosynthesis",
        "Who was Quaid-e-Azam?",
        "When is my Math exam?",
        "When is my Computer Science exam?"
    ]

    for question in examples:

        if st.button(question, use_container_width=True):

            st.session_state.pending_question = question
            st.rerun()

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()


st.markdown(
    '<div class="title">🎓 Study Buddy AI Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Learn Smarter • Prepare Better • Achieve More'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

if not st.session_state.messages:

    st.subheader("👋 Welcome, Student!")

    st.write(
        "I am your AI Study Buddy. "
        "Ask questions, explore educational topics "
        "or check your upcoming exams."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📖 **LEARN**\n\nUnderstand new topics.")

    with col2:
        st.info("📅 **EXAMS**\n\nCheck exam dates.")

    with col3:
        st.info("🔎 **RESEARCH**\n\nExplore Wikipedia.")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("tools"):

            with st.expander("🔧 Tools Used"):

                for tool_name in message["tools"]:
                    st.write(f"✅ {tool_name}")

prompt = st.chat_input("Ask Study Buddy anything...")

if st.session_state.pending_question:

    prompt = st.session_state.pending_question
    st.session_state.pending_question = None


if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    conversation = [
        {
            "role": msg["role"],
            "content": msg["content"]
        }
        for msg in st.session_state.messages
    ]

    with st.chat_message("assistant"):

        with st.spinner("🤖 Study Buddy is thinking..."):

            try:

                result = agent.invoke({
                    "messages": conversation
                })

                answer = result["messages"][-1].content

                if isinstance(answer, list):

                    answer = "\n".join(
                        str(item.get("text", item))
                        if isinstance(item, dict)
                        else str(item)
                        for item in answer
                    )

                tools_used = []

                for message in result["messages"]:

                    if message.type == "ai" and message.tool_calls:

                        for call in message.tool_calls:
                            tools_used.append(call["name"])

                st.markdown(answer)

                if tools_used:

                    with st.expander("🔧 Tools Used"):

                        for name in tools_used:
                            st.write(f"✅ {name}")

                else:
                    st.caption("No external tools were needed.")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "tools": tools_used
                })

            except Exception as e:

                st.error(f"Something went wrong: {str(e)}")

st.divider()

st.markdown(
    "<p style='text-align:center;color:#94A3B8;'>"
    "🎓 Study Buddy AI | Powered by Groq + LangChain + Streamlit"
    "</p>",
    unsafe_allow_html=True
)
