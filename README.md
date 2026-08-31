# AI Resume & Career Advisor

## 📌 Project Description

AI Resume & Career Advisor is a Generative AI based system that analyzes a candidate's resume and provides personalized career guidance.

The system extracts information from a resume, identifies the candidate's skills, retrieves relevant job descriptions using Retrieval-Augmented Generation (RAG), performs skill gap analysis, and generates personalized career recommendations using an AI Agent.

The system also provides interview preparation and a personalized 3-month learning roadmap.

---

## ✨ Features

- 📄 Resume PDF Analysis
- 🧠 AI-powered Resume Analysis
- 🔎 RAG-based Job Description Retrieval
- 🎯 Skill Gap Analysis
- 📊 Resume-to-Job Match Score
- ✅ Matching Skills Identification
- ❌ Missing Skills Identification
- 🤖 AI Career Advisor
- 🎤 Interview Preparation
- 📚 Personalized 3-Month Learning Roadmap
- 🖥️ Interactive Streamlit Interface
- 🔗 n8n AI Agent Integration

---

## 🛠️ Technology Stack

### Frontend
- Streamlit

### Backend
- Python

### AI / LLM
- Groq
- GPT-OSS-120B
- LangChain

### RAG
- FAISS
- LangChain
- Job Description PDFs

### AI Agent & Automation
- n8n
- n8n AI Agent

### Development Tools
- VS Code
- Git
- GitHub

---

## 🏗️ System Workflow

```text
Resume PDF
    ↓
PDF Text Extraction
    ↓
Resume Analyzer
    ↓
Candidate Skills & Information
    ↓
RAG + FAISS
    ↓
Relevant Job Description
    ↓
Skill Gap Analysis
    ↓
n8n Webhook
    ↓
AI Career Advisor Agent
    ↓
GPT-OSS-120B
    ↓
Career Advice
    ↓
Resume Feedback
Skill Gap
Interview Preparation
3-Month Learning Roadmap
