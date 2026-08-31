import os
import sys
import tempfile
import requests
import streamlit as st

# ============================================================
# ADD SRC FOLDER TO PYTHON PATH
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from dotenv import load_dotenv

from pdf_reader import extract_text_from_pdf
from resume_analyzer import analyze_resume
from rag import search_jobs
from skill_gap import analyze_skill_gap


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)

N8N_WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL"
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume & Career Advisor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background:
        linear-gradient(
            135deg,
            #f8fafc 0%,
            #eef2ff 50%,
            #f8fafc 100%
        );
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

* {
    box-sizing: border-box;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    background:
        linear-gradient(
            135deg,
            #111827,
            #1e3a8a
        );

    padding: 45px 50px;

    border-radius: 24px;

    margin-bottom: 30px;

    box-shadow:
        0 15px 40px
        rgba(30, 58, 138, 0.20);

    overflow: hidden;
}

.hero h1 {
    color: #ffffff !important;
    font-size: 44px !important;
    font-weight: 800 !important;
    margin: 0 0 12px 0 !important;
    line-height: 1.15 !important;
}

.hero p {
    color: #dbeafe !important;
    font-size: 18px !important;
    line-height: 1.6 !important;
    margin: 0 !important;
}


/* ============================================================
   CARDS
   ============================================================ */

.info-card {
    background: #ffffff;

    padding: 24px;

    border-radius: 18px;

    border: 1px solid #e5e7eb;

    box-shadow:
        0 8px 25px
        rgba(15, 23, 42, 0.06);

    margin-bottom: 20px;

    overflow-wrap: anywhere;

    word-break: break-word;
}


/* ============================================================
   UPLOAD CARD
   ============================================================ */

.upload-card {
    background: #ffffff;

    padding: 28px;

    border-radius: 20px;

    border: 1px solid #e5e7eb;

    box-shadow:
        0 8px 25px
        rgba(15, 23, 42, 0.06);

    margin-bottom: 25px;
}

.upload-title {
    font-size: 27px;

    font-weight: 750;

    color: #111827;

    margin-bottom: 8px;
}

.upload-description {
    color: #64748b;

    font-size: 15px;

    margin-bottom: 20px;
}


/* ============================================================
   SECTION TITLES
   ============================================================ */

.section-title {
    font-size: 28px;

    font-weight: 750;

    color: #111827;

    margin-top: 30px;

    margin-bottom: 18px;

    line-height: 1.25;
}


/* ============================================================
   SKILL BADGES
   ============================================================ */

.skill-badge {
    display: inline-block;

    background: #dbeafe;

    color: #1e3a8a;

    padding: 8px 14px;

    border-radius: 30px;

    margin: 4px;

    font-size: 14px;

    font-weight: 600;

    border: 1px solid #bfdbfe;

    max-width: 100%;

    overflow-wrap: anywhere;
}

.missing-badge {
    display: inline-block;

    background: #fee2e2;

    color: #991b1b;

    padding: 8px 14px;

    border-radius: 30px;

    margin: 4px;

    font-size: 14px;

    font-weight: 600;

    border: 1px solid #fecaca;

    max-width: 100%;

    overflow-wrap: anywhere;
}


/* ============================================================
   SCORE CARDS
   ============================================================ */

.score-box {
    text-align: center;

    background: #ffffff;

    padding: 25px;

    border-radius: 18px;

    border: 1px solid #e5e7eb;

    box-shadow:
        0 8px 25px
        rgba(15, 23, 42, 0.06);

    min-height: 115px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    width: 100%;
}

.score-number {
    font-size: 42px;

    font-weight: 800;

    color: #1d4ed8;

    line-height: 1.1;
}

.score-label {
    font-size: 14px;

    color: #64748b;

    font-weight: 600;

    margin-top: 8px;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {

    background: #f8fafc;

    border-radius: 16px;

    padding: 12px;

    border: 2px dashed #bfdbfe;

    width: 100%;
}


/* ============================================================
   BUTTON
   ============================================================ */

.stButton > button {

    width: 100%;

    border-radius: 12px;

    padding: 13px 20px;

    font-size: 16px;

    font-weight: 700;

    border: none;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #4f46e5
        );

    color: white;

    transition: 0.2s;

    min-height: 48px;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 20px
        rgba(37, 99, 235, 0.25);
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {

    background: #ffffff;

    border-right:
        1px solid #e5e7eb;
}


/* ============================================================
   TABLET
   ============================================================ */

@media (max-width: 900px) {

    .block-container {

        padding-left: 1.2rem;

        padding-right: 1.2rem;

        padding-top: 1.5rem;
    }

    .hero {

        padding: 35px 30px;

    }

    .hero h1 {

        font-size: 36px !important;

    }

    .hero p {

        font-size: 17px !important;

    }

    .upload-card {

        padding: 23px;

    }

    .section-title {

        font-size: 25px;

    }

}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 640px) {

    .block-container {

        max-width: 100% !important;

        padding-top: 0.8rem !important;

        padding-bottom: 2rem !important;

        padding-left: 0.75rem !important;

        padding-right: 0.75rem !important;
    }


    /* HERO */

    .hero {

        padding: 25px 18px !important;

        border-radius: 17px !important;

        margin-bottom: 18px !important;

    }

    .hero h1 {

        font-size: 27px !important;

        line-height: 1.2 !important;

        margin-bottom: 10px !important;

    }

    .hero p {

        font-size: 14px !important;

        line-height: 1.55 !important;

    }


    /* UPLOAD CARD */

    .upload-card {

        padding: 17px !important;

        border-radius: 16px !important;

        margin-bottom: 18px !important;
    }

    .upload-title {

        font-size: 22px !important;

    }

    .upload-description {

        font-size: 13px !important;

        line-height: 1.5 !important;

    }


    /* INFO CARDS */

    .info-card {

        padding: 16px !important;

        border-radius: 15px !important;

        margin-bottom: 14px !important;

    }


    /* SECTION TITLES */

    .section-title {

        font-size: 22px !important;

        margin-top: 22px !important;

        margin-bottom: 12px !important;

    }


    /* SCORE */

    .score-box {

        padding: 18px 10px !important;

        min-height: 95px !important;

        margin-bottom: 10px !important;

    }

    .score-number {

        font-size: 32px !important;

    }

    .score-label {

        font-size: 11px !important;

        margin-top: 6px !important;

    }


    /* SKILLS */

    .skill-badge,
    .missing-badge {

        font-size: 12px !important;

        padding: 7px 10px !important;

        margin: 3px !important;

    }


    /* BUTTON */

    .stButton > button {

        font-size: 15px !important;

        padding: 10px 12px !important;

        min-height: 46px !important;

    }


    /* UPLOADER */

    [data-testid="stFileUploader"] {

        padding: 7px !important;

        border-radius: 13px !important;

    }


    /* ALERTS */

    [data-testid="stAlert"] {

        font-size: 13px !important;

    }


    /* TEXT */

    p {

        overflow-wrap: anywhere !important;

        word-break: break-word !important;

    }

    .stMarkdown {

        overflow-wrap: anywhere !important;

        word-break: break-word !important;

    }


    /* HEADINGS */

    h1 {

        font-size: 27px !important;

    }

    h2 {

        font-size: 22px !important;

    }

    h3 {

        font-size: 18px !important;

    }

}


/* ============================================================
   VERY SMALL PHONES
   ============================================================ */

@media (max-width: 380px) {

    .block-container {

        padding-left: 0.55rem !important;

        padding-right: 0.55rem !important;

    }

    .hero {

        padding: 22px 15px !important;

    }

    .hero h1 {

        font-size: 24px !important;

    }

    .hero p {

        font-size: 13px !important;

    }

    .upload-title {

        font-size: 20px !important;

    }

    .score-number {

        font-size: 29px !important;

    }

    .score-label {

        font-size: 10px !important;

    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    '<div class="hero">'
    '<h1>🚀 AI Resume &amp; Career Advisor</h1>'
    '<p>Analyze your resume, discover skill gaps, identify suitable career opportunities and get an AI-powered personalized learning roadmap.</p>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# MAIN UPLOAD SECTION
# ============================================================

st.markdown(
    '<div class="upload-card">'
    '<div class="upload-title">📄 Upload Your Resume</div>'
    '<div class="upload-description">'
    'Upload your resume PDF and select the job role you want to target.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


uploaded_file = st.file_uploader(
    "📄 Choose your resume PDF",
    type=["pdf"],
    help="Upload a PDF version of your resume."
)


target_role = st.selectbox(
    "🎯 Target Job Role",
    [
        "Automatic",
        "Python Developer",
        "Data Analyst",
        "AI / ML Engineer",
        "Software Developer",
        "Full Stack Web Developer"
    ]
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if uploaded_file:

    st.success(
        f"✅ Resume uploaded: {uploaded_file.name}"
    )

    analyze_button = st.button(
        "🚀 Analyze My Resume",
        use_container_width=True
    )

else:

    analyze_button = False


# ============================================================
# EMPTY STATE
# ============================================================

if uploaded_file is None:

    st.markdown(
        '<div class="info-card">'
        '<h2>🎯 What You Will Get</h2>'
        '<p>'
        'Our AI system will analyze your resume, compare your '
        'skills with relevant job requirements and generate '
        'personalized career guidance.'
        '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "📊 Resume Score\n\n"
            "Understand how well your resume "
            "matches the selected role."
        )

    with col2:

        st.info(
            "🎯 Skill Gap\n\n"
            "Identify important skills "
            "you need to develop."
        )

    with col3:

        st.info(
            "🤖 AI Roadmap\n\n"
            "Get personalized interview "
            "and learning guidance."
        )


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    if not N8N_WEBHOOK_URL:

        st.error(
            "N8N_WEBHOOK_URL is missing."
        )

        st.stop()


    temp_path = None


    try:

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        progress = st.progress(0)

        status = st.empty()


        # ----------------------------------------------------
        # SAVE PDF
        # ----------------------------------------------------

        status.info(
            "📄 Reading your resume..."
        )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(
                uploaded_file.getvalue()
            )

            temp_path = temp_file.name


        progress.progress(15)


        # ----------------------------------------------------
        # EXTRACT TEXT
        # ----------------------------------------------------

        status.info(
            "🔍 Extracting resume information..."
        )

        resume_text = extract_text_from_pdf(
            temp_path
        )

        progress.progress(30)


        # ----------------------------------------------------
        # RESUME ANALYSIS
        # ----------------------------------------------------

        status.info(
            "🧠 AI is analyzing your resume..."
        )

        resume_data = analyze_resume(
            resume_text
        )

        progress.progress(45)


        # ----------------------------------------------------
        # RAG SEARCH
        # ----------------------------------------------------

        status.info(
            "🔎 Finding the most relevant job description..."
        )


        if target_role == "Automatic":

            query = f"""
            Candidate skills:
            {", ".join(resume_data.skills)}

            Find the most suitable job role
            for this candidate.
            """

        else:

            query = f"""
            Target job role:
            {target_role}

            Candidate skills:
            {", ".join(resume_data.skills)}
            """


        results = search_jobs(
            query,
            k=1
        )


        if results:

            job_description = (
                results[0].page_content
            )

            job_source = (
                results[0]
                .metadata
                .get(
                    "source",
                    "Unknown"
                )
            )

        else:

            job_description = ""

            job_source = "No job description found"


        progress.progress(60)


        # ----------------------------------------------------
        # SKILL GAP
        # ----------------------------------------------------

        status.info(
            "🎯 Calculating your skill gap..."
        )

        skill_gap = analyze_skill_gap(
            resume_data,
            job_description
        )

        progress.progress(75)


        # ----------------------------------------------------
        # PREPARE N8N PAYLOAD
        # ----------------------------------------------------

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

            "job_role": skill_gap.get(
                "job_role",
                target_role
            ),

            "match_percentage": skill_gap.get(
                "match_percentage",
                0
            ),

            "matching_skills": skill_gap.get(
                "matching_skills",
                []
            ),

            "missing_skills": skill_gap.get(
                "missing_skills",
                []
            ),

            "additional_recommendations":
                skill_gap.get(
                    "additional_recommendations",
                    []
                ),

            "overall_feedback":
                skill_gap.get(
                    "overall_feedback",
                    ""
                ),

            "job_description":
                job_description
        }


        # ----------------------------------------------------
        # SEND TO N8N
        # ----------------------------------------------------

        status.info(
            "🤖 Career Advisor Agent is preparing your advice..."
        )


        n8n_response = requests.post(

            N8N_WEBHOOK_URL,

            json=payload,

            timeout=120

        )


        progress.progress(90)


        # ----------------------------------------------------
        # HANDLE N8N RESPONSE
        # ----------------------------------------------------

        if n8n_response.status_code == 200:

            try:

                n8n_data = (
                    n8n_response.json()
                )

                career_advice = (
                    n8n_data.get(
                        "career_advice",
                        ""
                    )
                )

            except Exception:

                career_advice = (
                    n8n_response.text
                )

        else:

            career_advice = (
                "Career Advisor service "
                "returned an error."
            )


        # ----------------------------------------------------
        # SAVE RESULTS
        # ----------------------------------------------------

        st.session_state[
            "resume"
        ] = resume_data

        st.session_state[
            "skill_gap"
        ] = skill_gap

        st.session_state[
            "career_advice"
        ] = career_advice

        st.session_state[
            "job_source"
        ] = job_source


        progress.progress(100)

        status.success(
            "✅ Analysis completed successfully!"
        )


    except Exception as error:

        st.error(
            "❌ Something went wrong during analysis."
        )

        st.exception(
            error
        )


    finally:

        if temp_path and os.path.exists(
            temp_path
        ):

            os.remove(
                temp_path
            )


# ============================================================
# DISPLAY RESULTS
# ============================================================

if "resume" in st.session_state:

    resume = st.session_state[
        "resume"
    ]

    gap = st.session_state[
        "skill_gap"
    ]

    career_advice = st.session_state[
        "career_advice"
    ]

    job_source = st.session_state[
        "job_source"
    ]


    # ========================================================
    # CANDIDATE HEADER
    # ========================================================

    st.markdown(
        f'<div class="info-card">'
        f'<h1>👋 Hello, {resume.name}</h1>'
        f'<p>Here\'s your AI-powered resume and career analysis.</p>'
        f'</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SCORE CARDS
    # ========================================================

    st.markdown(
        '<div class="section-title">📊 Resume Overview</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        match = gap.get(
            "match_percentage",
            0
        )

        st.markdown(
            f'<div class="score-box">'
            f'<div class="score-number">{match}%</div>'
            f'<div class="score-label">JOB MATCH</div>'
            f'</div>',
            unsafe_allow_html=True
        )


    with col2:

        matching_count = len(
            gap.get(
                "matching_skills",
                []
            )
        )

        st.markdown(
            f'<div class="score-box">'
            f'<div class="score-number">{matching_count}</div>'
            f'<div class="score-label">MATCHING SKILLS</div>'
            f'</div>',
            unsafe_allow_html=True
        )


    with col3:

        missing_count = len(
            gap.get(
                "missing_skills",
                []
            )
        )

        st.markdown(
            f'<div class="score-box">'
            f'<div class="score-number">{missing_count}</div>'
            f'<div class="score-label">SKILLS TO LEARN</div>'
            f'</div>',
            unsafe_allow_html=True
        )


    # ========================================================
    # CURRENT SKILLS
    # ========================================================

    st.markdown(
        '<div class="section-title">💻 Your Skills</div>',
        unsafe_allow_html=True
    )


    skills_html = ""


    for skill in resume.skills:

        skills_html += (
            f'<span class="skill-badge">'
            f'{skill}'
            f'</span>'
        )


    st.markdown(
        f'<div class="info-card">{skills_html}</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SKILL GAP
    # ========================================================

    st.markdown(
        '<div class="section-title">🎯 Skill Gap Analysis</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "✅ Matching Skills"
        )

        matching_skills = gap.get(
            "matching_skills",
            []
        )

        if matching_skills:

            for skill in matching_skills:

                st.markdown(
                    f'<span class="skill-badge">'
                    f'✓ {skill}'
                    f'</span>',
                    unsafe_allow_html=True
                )

        else:

            st.write(
                "No matching skills found."
            )


    with col2:

        st.subheader(
            "❌ Missing Skills"
        )

        missing_skills = gap.get(
            "missing_skills",
            []
        )

        if missing_skills:

            for skill in missing_skills:

                st.markdown(
                    f'<span class="missing-badge">'
                    f'{skill}'
                    f'</span>',
                    unsafe_allow_html=True
                )

        else:

            st.success(
                "No major skill gaps detected!"
            )


    # ========================================================
    # RESUME FEEDBACK
    # ========================================================

    st.markdown(
        '<div class="section-title">📝 Resume Feedback</div>',
        unsafe_allow_html=True
    )


    feedback = gap.get(
        "overall_feedback",
        "No feedback available."
    )


    st.markdown(
        f'<div class="info-card">{feedback}</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.markdown(
        '<div class="section-title">💡 Recommendations</div>',
        unsafe_allow_html=True
    )


    recommendations = gap.get(
        "additional_recommendations",
        []
    )


    if recommendations:

        for recommendation in recommendations:

            st.info(
                f"👉 {recommendation}"
            )

    else:

        st.write(
            "No additional recommendations."
        )


    # ========================================================
    # AI CAREER ADVISOR
    # ========================================================

    st.markdown(
        '<div class="section-title">🤖 AI Career Advisor</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        f'<div class="info-card">{career_advice}</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # JOB SOURCE
    # ========================================================

    st.caption(
        f"🔎 Job Description Source: {job_source}"
    )