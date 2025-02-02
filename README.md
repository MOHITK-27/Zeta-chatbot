# ZETA - AI Chatbot 🤖

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-00FF00?style=for-the-badge&logo=groq&logoColor=black)](https://groq.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

An intelligent chatbot with personality, powered by Groq's ultra-fast LLMs and Streamlit's interactive interface.

![Chatbot Demo](screenshots/demo.gif) <!-- Add actual screenshot path -->

## Features ✨

- **Dynamic Personality**: 100+ predefined witty responses
- **Multi-Model Support**: Switch between different LLMs
- **Markdown Editor**: Rich text composition with live preview
- **Chat History**: Save/Load multiple conversation sessions
- **Fun Interactions**: Confetti, snow effects & random facts
- **Error Resilience**: Graceful error handling with humor
- **Message Analytics**: Real-time conversation statistics

## Installation 🛠️

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/zeta-chatbot.git
cd zeta-chatbot
Install Dependencies

bash
Copy
pip install -r requirements.txt
Configure Environment

bash
Copy
cp .env.example .env
# Add your Groq API key to .env
Run Application

bash
Copy
streamlit run app.py
Configuration ⚙️
Create .streamlit/secrets.toml with:

toml
Copy
GROQ_API_KEY = "your-api-key-here"
Usage Guide 🚀
Launch Interface

bash
Copy
streamlit run app.py
Model Selection

Choose from supported LLMs in sidebar

Compose Message

Use Markdown editor for rich formatting

Click 🚀 Send or press Ctrl+Enter

Manage Chats

Create new sessions with ➕ New Chat

Load previous conversations from history

Fun Features

Trigger confetti/snow effects

Get random tech facts

Export chat history

Project Structure 📂
Copy
zeta-chatbot/
├── app.py               # Main application
├── pr.py                # Predefined responses
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
└── screenshots/         # Demo images
Roadmap 🗺️
Voice Input/Output

Multi-language Support

API Rate Limiting

User Authentication

Multi-modal Integration

Contributing 🤝
Fork the repository

Create your feature branch

Commit changes

Push to the branch

Open a Pull Request

License 📄
Distributed under MIT License. See LICENSE for details.
Not for commercial purposes 

Acknowledgments 🙏

Powered by Groq API

Built with Streamlit

Developed by Mohit 💻
