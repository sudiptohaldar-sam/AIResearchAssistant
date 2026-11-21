# 🔬 AI Research Assistant

An AI-powered research assistant that automates the process of researching a topic, gathering information from the web, generating a structured report, and reviewing its quality using AI agents.

## 🚀 About the Project

This project uses a multi-agent AI workflow to simplify research. Given a topic, it searches the web for relevant information, extracts detailed content from selected resources, generates a research report, and evaluates the report using an AI critic.

The entire process is presented through an interactive Streamlit dashboard.

## 🤖 Workflow

- 🔎 **Search Agent:** Searches the web for relevant and recent information using Tavily.
- 📖 **Reader Agent:** Extracts useful information from relevant webpages.
- ✍️ **Writer Agent:** Generates a structured research report based on the collected information.
- 🧐 **Critic Agent:** Reviews the report and provides a score, strengths, weaknesses, and suggestions for improvement.

## 🛠️ Tech Stack

- Python
- LangChain
- Groq
- Tavily
- Requests
- BeautifulSoup
- Streamlit

## ✨ Features

- Automated multi-agent research workflow
- Web search and content extraction
- AI-generated research reports
- AI-powered report evaluation
- Interactive Streamlit dashboard
- Research report download


## 🔮 Future Improvements

- Multi-source research
- Source citations
- Critic-driven report refinement
- Research history and memory
