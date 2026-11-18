# 🎓 Study Buddy AI Agent

**Your Personal AI Learning Assistant**

Study Buddy AI is an intelligent educational chatbot built using **Python, Streamlit, LangChain, and Groq AI**. It helps students understand difficult topics, search for educational information, and check upcoming examination dates through an AI-powered agent.

## 🚀 Features

- 💬 **AI Chat:** Ask questions and get simple, understandable answers.
- 📚 **Educational Assistance:** Learn and understand difficult school subjects.
- 📅 **Exam Information:** Check upcoming examination dates and remaining days.
- 🔍 **Wikipedia Search:** Retrieve educational information from Wikipedia.
- 🤖 **AI Agent:** Uses LangChain to decide when external tools are needed.
- 🎨 **Modern UI:** Beautiful dark-themed interface built with Streamlit.
- 🗑️ **Chat Management:** Clear conversation history whenever needed.
- 🔧 **Tool Tracking:** View which tools the AI agent uses to answer questions.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| LangChain | AI agent development |
| Groq | AI language model |
| Wikipedia | Educational information retrieval |
| Python-dotenv | Environment variable management |

## 📂 Project Structure

```text
Study-Buddy-AI/
│
├── app.py              # Main Streamlit application
├── .env                # Groq API key (private)
├── .gitignore          # Files excluded from GitHub
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Study-Buddy-AI.git
```

### 2. Navigate to the Project Folder

```bash
cd Study-Buddy-AI
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Configure Your Groq API Key

Create a file named `.env` in the project directory.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from:

https://console.groq.com/keys

**Important:** Never upload your `.env` file or share your API key publicly.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your web browser.

## 📦 Requirements

Create a `requirements.txt` file containing:

```text
streamlit
wikipedia
python-dotenv
langchain
langchain-groq
```

## 💡 Example Questions

Try asking Study Buddy:

- When is my Science exam?
- Explain photosynthesis.
- Who was Quaid-e-Azam?
- When is my Math exam?
- Explain artificial intelligence.
- When is my Computer Science exam?

## 📅 Exam Schedule

The application currently uses predefined exam offsets:

| Subject | Days from Today |
|---|---:|
| Mathematics | 5 days |
| Science | 9 days |
| English | 12 days |
| Computer Science | 15 days |

*Note: These are example dates calculated dynamically from the current date, not official examination dates.*

## 🔐 Environment Variables

The application uses `python-dotenv` to securely load the Groq API key from the `.env` file.

Example:

```python
from dotenv import load_dotenv
import os

load_dotenv(override=True)

API_KEY = os.getenv("GROQ_API_KEY")
```

## 🔮 Future Improvements

- Add a personalized study timetable.
- Integrate PDF question answering.
- Add quiz and practice test generation.
- Include subject-wise learning progress.
- Add a real examination timetable.
- Implement persistent chat history.

## 👨‍💻 Developer

**Muhammad Rayyan Khan**

Developed with ❤️ using Python, Streamlit, LangChain, and Groq AI.

---

⭐ If you find this project useful, consider giving it a star on GitHub!

**Study Buddy AI – Learn Smarter, Prepare Better, Achieve More!**
