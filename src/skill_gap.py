import os
import json
import requests

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from resume_analyzer import analyze_resume
from pdf_reader import extract_text_from_pdf
from rag import search_jobs


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


# ==========================================
# INITIALIZE LLM
# ==========================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================
# SKILL GAP PROMPT
# ==========================================

prompt = ChatPromptTemplate.from_template("""
You are an expert technical recruiter and career advisor.

Compare the candidate's resume skills with the requirements
of the job description.

CANDIDATE RESUME:

Name:
{candidate_name}

Skills:
{candidate_skills}

Education:
{education}

Projects:
{projects}


JOB DESCRIPTION:

{job_description}


Return ONLY valid JSON using this structure:

{{
    "job_role": "",
    "match_percentage": 0,
    "matching_skills": [],
    "missing_skills": [],
    "additional_recommendations": [],
    "overall_feedback": ""
}}

Rules:

- Compare the candidate's actual skills with the job requirements.
- Do not invent candidate skills.
- matching_skills must contain skills present in both the resume and job requirements.
- missing_skills must contain important job skills absent from the resume.
- match_percentage must be between 0 and 100.
- Give practical recommendations.
- Return ONLY JSON.
""")


# ==========================================
# SKILL GAP ANALYSIS
# ==========================================

def analyze_skill_gap(resume_data, job_description):

    candidate_name = resume_data.name

    candidate_skills = ", ".join(
        resume_data.skills
    )

    education = ", ".join(
        resume_data.education
    )

    projects = "\n".join(
        [
            f"{project.name}: {project.description}"
            for project in resume_data.projects
        ]
    )

    messages = prompt.format_messages(
        candidate_name=candidate_name,
        candidate_skills=candidate_skills,
        education=education,
        projects=projects,
        job_description=job_description
    )

    response = llm.invoke(messages)

    content = response.content.strip()

    # Remove markdown JSON formatting
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    return json.loads(content)


# ==========================================
# SEND DATA TO N8N
# ==========================================

def send_to_n8n(resume_data, result, job_description):

    print("\n5. Sending data to n8n...")

    if not N8N_WEBHOOK_URL:
        print("ERROR: N8N_WEBHOOK_URL not found in .env")
        return

    payload = {
        "name": resume_data.name,

        "skills": resume_data.skills,

        "education": resume_data.education,

        "projects": [
            {
                "name": project.name,
                "description": project.description
            }
            for project in resume_data.projects
        ],

        "job_role": result.get(
            "job_role",
            ""
        ),

        "match_percentage": result.get(
            "match_percentage",
            0
        ),

        "matching_skills": result.get(
            "matching_skills",
            []
        ),

        "missing_skills": result.get(
            "missing_skills",
            []
        ),

        "additional_recommendations": result.get(
            "additional_recommendations",
            []
        ),

        "overall_feedback": result.get(
            "overall_feedback",
            ""
        ),

        "job_description": job_description
    }

    print("\nData being sent to n8n:")

    print(
        json.dumps(
            payload,
            indent=4
        )
    )

    try:

        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=120
        )

        print("\n================================")
        print("          N8N RESPONSE")
        print("================================")

        print(
            "n8n Status Code:",
            response.status_code
        )

        print("\nResponse:")

        print(
            response.text
        )

    except requests.exceptions.RequestException as error:

        print("\nERROR connecting to n8n:")

        print(error)


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("\n================================")
    print("       AI CAREER ADVISOR")
    print("================================\n")


    # --------------------------------------
    # STEP 1: READ RESUME
    # --------------------------------------

    print("1. Reading resume...")

    resume_text = extract_text_from_pdf(
        "data/resume.pdf"
    )

    print("Resume extracted.")


    # --------------------------------------
    # STEP 2: ANALYZE RESUME
    # --------------------------------------

    print("\n2. Analyzing resume...")

    resume_data = analyze_resume(
        resume_text
    )

    print("Resume analysis completed.")

    print("\nCandidate:")
    print(resume_data.name)

    print("\nSkills:")

    print(
        ", ".join(
            resume_data.skills
        )
    )


    # --------------------------------------
    # STEP 3: SEARCH RELEVANT JOB
    # --------------------------------------

    print("\n3. Searching relevant jobs...")

    skill_query = f"""
    Candidate skills:
    {", ".join(resume_data.skills)}

    Find the most suitable job description
    based on these skills.
    """

    results = search_jobs(
        skill_query,
        k=1
    )


    if not results:

        print(
            "No relevant job description found."
        )

        exit()


    # --------------------------------------
    # STEP 4: GET JOB DESCRIPTION
    # --------------------------------------

    job = results[0]

    job_description = job.page_content

    job_source = job.metadata.get(
        "source",
        "Unknown"
    )

    print("\nRelevant Job Found:")

    print(job_source)


    # --------------------------------------
    # STEP 5: SKILL GAP ANALYSIS
    # --------------------------------------

    print("\n4. Analyzing skill gap...")

    result = analyze_skill_gap(
        resume_data,
        job_description
    )


    print("\n================================")
    print("       SKILL GAP ANALYSIS")
    print("================================\n")

    print(
        json.dumps(
            result,
            indent=4
        )
    )


    # --------------------------------------
    # STEP 6: SEND TO N8N
    # --------------------------------------

    send_to_n8n(
        resume_data,
        result,
        job_description
    )