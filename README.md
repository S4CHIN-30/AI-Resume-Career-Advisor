# 🚀 AI Resume & Career Advisor

AI-powered Resume & Career Advisor that analyzes resumes, identifies skill gaps, matches candidates with relevant job roles, and provides personalized career guidance.

## 🌐 Live Demo

👉 **[Open AI Resume & Career Advisor](https://ai-resume-career-advisor.streamlit.app/)**

## 📂 GitHub Repository

👉 **[View Source Code](https://github.com/S4CHIN-30/AI-Resume-Career-Advisor)**

## ✨ Features

- 📄 Resume PDF Upload
- 🧠 AI-powered Resume Analysis
- 📊 Resume-to-Job Match Score
- 🎯 Skill Gap Analysis
- 💻 Matching & Missing Skills
- 🔎 Job Description Retrieval using RAG
- ⚡ FAISS Vector Search
- 🤖 AI Career Advisor
- 💡 Personalized Recommendations
- 🗺️ Career & Learning Roadmap
- 📱 Responsive UI for Desktop and Mobile

## 🛠️ Tech Stack

- Python
- Streamlit
- Groq
- GPT-OSS-120B
- LangChain
- RAG
- FAISS
- n8n
- PyPDF
- Requests

## 🔄 How It Works

1. Upload your resume PDF.
2. Select your target job role.
3. Resume text is extracted.
4. AI analyzes your resume.
5. RAG + FAISS retrieves a relevant job description.
6. The system compares your skills with job requirements.
7. Skill gaps are identified.
8. n8n AI Agent generates personalized career advice.
9. Results are displayed through the Streamlit interface.

## 📁 Project Structure

```text
AI-Resume-Career-Advisor/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── job_descriptions/
│
├── src/
│   ├── pdf_reader.py
│   ├── resume_analyzer.py
│   ├── rag.py
│   ├── skill_gap.py
│
└── vectorstore/
    └── job_descriptions/