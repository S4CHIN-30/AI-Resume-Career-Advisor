import os
import json

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from pdf_reader import extract_text_from_pdf


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# PYDANTIC DATA MODELS
# ==========================================

class Project(BaseModel):
    name: str = ""
    description: str = ""


class Experience(BaseModel):
    company: str = ""
    role: str = ""
    duration: str = ""


class ResumeData(BaseModel):
    name: str = ""
    education: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)


# ==========================================
# INITIALIZE LLM
# ==========================================

print("Resume Analyzer Started...")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================
# PROMPT ENGINEERING
# ==========================================

prompt = ChatPromptTemplate.from_template("""
You are an expert resume analyzer and career advisor.

Analyze the resume provided below carefully.

RESUME:
{resume_text}

Extract the following information:

1. Name
2. Education
3. Technical Skills
4. Projects
5. Work Experience
6. Certifications
7. Achievements

Return ONLY valid JSON using exactly this structure:

{{
    "name": "",
    "education": [],
    "skills": [],
    "projects": [
        {{
            "name": "",
            "description": ""
        }}
    ],
    "experience": [
        {{
            "company": "",
            "role": "",
            "duration": ""
        }}
    ],
    "certifications": [],
    "achievements": []
}}

Rules:

- Use ONLY information present in the resume.
- Do NOT invent or assume information.
- If information is not available, use an empty string or empty array.
- Skills must be listed individually.
- Each project must have a name and description.
- Each experience entry must contain company, role and duration when available.
- Keep the information concise.
- Return ONLY JSON.
""")


# ==========================================
# RESUME ANALYZER FUNCTION
# ==========================================

def analyze_resume(resume_text):

    messages = prompt.format_messages(
        resume_text=resume_text
    )

    response = llm.invoke(messages)

    content = response.content.strip()

    # Remove markdown code block if returned by LLM
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    # Convert JSON string into Python dictionary
    data = json.loads(content)

    # Validate using Pydantic
    validated_data = ResumeData(**data)

    return validated_data


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("Reading resume...")

    resume_text = extract_text_from_pdf(
        "data/resume.pdf"
    )

    print("Resume text extracted!")

    print("Calling LLM...")

    result = analyze_resume(resume_text)

    print("LLM response received!")

    print("\n================================")
    print("        RESUME ANALYSIS")
    print("================================\n")

    print(result.model_dump_json(indent=4))