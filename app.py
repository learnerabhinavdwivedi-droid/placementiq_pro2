import streamlit as st
import numpy as np
import joblib
import pandas as pd
import pdfplumber
import time
import base64
import streamlit as st

from openai import OpenAI


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Use your image file name here
img_base64 = get_base64_image("Gemini_Generated_Image_6dai4k6dai4k6dai.png")


st.sidebar.markdown(
    f"""
    <style>
    /* Positions the logo in the top blank space of the sidebar */
    [data-testid="stSidebarNav"]::before {{
        content: "";
        display: block;
        margin-top: 20px;
    }}
    
    .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        perspective: 1000px; /* Essential for 3D depth */
        margin-bottom: 20px;
    }}

    .logo-3d {{
        width: 150px; /* Adjust size as needed */
        transition: transform 1.2s cubic-bezier(0.4, 0, 0.2, 1); /* Smooth rotation */
        transform-style: preserve-3d;
        filter: drop-shadow(0 10px 20px rgba(0,0,0,0.4)); /* Adds 3D floating effect */
    }}

    /* The 360-degree rotation on hover */
    .logo-container:hover .logo-3d {{
        transform: rotateY(360deg) scale(1.1); /* Full spin + slight zoom */
    }}
    </style>

    <div class="logo-container">
        <img src="data:image/png;base64,{img_base64}" class="logo-3d">
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<style>

/* GLOBAL FONT */
html, body, [class*="css"] {
    font-family: 'Segoe UI', Roboto, sans-serif;
}

/* BACKGROUND */
body {
    background-color: #f6f8fc;
}

/* Analyze Button Base */
div.stButton > button {
    background: linear-gradient(90deg,#2563eb,#1e40af);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-size: 17px;
    border: none;
    transition: all 0.25s ease;
}

/* Hover Effect (same as cards) */
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(0,0,0,0.18);
    background: linear-gradient(90deg,#1e40af,#1e3a8a);
}

/* Click Effect */
div.stButton > button:active {
    transform: scale(0.98);
}



/* CARD */
.card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    margin-bottom: 18px;
}

/* HERO HEADER */
.hero {
    background:#f4f7ff;
    color: #1f2a44;
    padding: 32px;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.2);

    transition: all 0.25s ease;
}

.hero:hover {
    transform: translateY(-3px);
    box-shadow: 0 18px 36px rgba(0,0,0,0.25);
    filter: brightness(1.05);
}

.hero-title {
    font-size: 36px;
    font-weight: 700;
}
.hero-sub {
    font-size: 18px;
}
.hero-desc {
    font-size: 14px;
    opacity: .85;
}


/* ---------- CARD HOVER EFFECT ---------- */
.card-hover {
    transition: all 0.25s ease;
    border: 1px solid transparent;
}

.card-hover:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.15);
    border: 1px solid rgba(31,119,180,0.25);
    box-shadow: 0 18px 40px rgba(0,0,0,0.2);
}
""", unsafe_allow_html=True)


# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="PlacementIQ",
    layout="wide"
)

# ---------------- LOAD MODEL SAFELY ----------------
try:
    model = joblib.load("placement_model.pkl")
except:
    st.error("Model file not found. Please run train_model.py first.")
    st.stop()

st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# -------- SIDEBAR (POLISHED DESIGN) --------
st.sidebar.markdown("""
<style>
.sidebar-card {
    background: #f4f7ff;
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 14px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.06);
}
.sidebar-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 2px;
}
.sidebar-sub {
    font-size: 13px;
    color: #555;
}
.sidebar-section {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 6px;
}
.sidebar-text {
    font-size: 14px;
    color: #333;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# --- Header Card ---
st.markdown("""
<div class="-card" style="text-align:center;">
    <div class="-title">PlacementIQ</div>
    <div class="sidebar-sub">AI Placement Readiness Analyzer</div>
    <div style="font-size:12px;margin-top:6px;">HackWave 2026 Project</div>
</div>
""", unsafe_allow_html=True)
# --- Chatbot Configuration ---
# Replace 'YOUR_GEMINI_API_KEY' with your actual key or use st.secrets





st.title("PlacementIQ AI Assistant")

#import streamlit as st
from openai import OpenAI

# 1. Force layout to be wide to accommodate the sidebar better
st.set_page_config(layout="wide")

import streamlit as st
from openai import OpenAI

# 1. Groq Setup
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=st.secrets["GROQ_API_KEY"]
)

# 2. Custom CSS for UI/UX (Matching your images)
st.markdown("""
    <style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #121212;
        color: white;
    }
    
    /* Clear Chat Button Styling */
    .clear-btn {
        background-color: #262626;
        color: #ffffff;
        border: 1px solid #444;
        border-radius: 5px;
        padding: 5px 10px;
        font-size: 14px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 5px;
        margin-bottom: 20px;
    }

    /* Chat Bubble Styling */
    .stChatMessage {
        background-color: transparent !important;
    }
    
    /* User Message (Right Aligned - Orange/Brown theme) */
    [data-testid="chatAvatarIcon-user"] {
        display: none;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"] > p:empty) { display:none; }
    
    .user-bubble {
        background-color: #4a3721;
        color: #ffcc80;
        border-radius: 20px;
        padding: 10px 15px;
        margin-left: auto;
        width: fit-content;
        max-width: 80%;
        border: 1px solid #5d4037;
        margin-bottom: 10px;
    }

    /* Assistant Message (Left Aligned - Red/Dark theme) */
    .assistant-bubble {
        background-color: #331a1a;
        color: #ef9a9a;
        border-radius: 20px;
        padding: 10px 15px;
        margin-right: auto;
        width: fit-content;
        max-width: 80%;
        border: 1px solid #4a2c2c;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Implementation
with st.sidebar:
    st.title("PlacementIQ AI")
    
    
    # Clear Chat Option
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.write("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat Container
    message_container = st.container(height=500, border=False)
    
    with message_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# 4. Chat Input Logic (Pinned to Sidebar bottom)
with st.sidebar:
    if prompt := st.chat_input("Ask PlacementIQ anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with message_container:
            st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)
            
            with st.chat_message("assistant"): # Placeholder for streaming
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    stream=True,
                )
                response = st.write_stream(stream)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun() # Refresh to apply custom bubble styling to the new response




# ---------------- MAIN HEADER ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 1rem;
}
.main-header {
    background: linear-gradient(90deg,#1f77b4,#0d47a1);
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    color: white;
    margin-top: 10px;
    margin-bottom: 25px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
}
.main-title {
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 6px;
}
.main-sub {
    font-size: 17px;
    margin-top: 2px;
}
.main-desc {
    font-size: 14px;
    margin-top: 6px;
    opacity: 0.9;
}
div.stButton > button {
    height:3em;
    font-size:18px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">PlacementIQ</div>
    <div class="hero-sub">AI Placement Readiness Analyzer</div>
    <div class="hero-desc">
        Enterprise-grade placement intelligence using machine learning
    </div>
</div>
""", unsafe_allow_html=True)




st.divider()

col1, col2, col3 = st.columns(3)

card_style_blue_1 = """
padding:22px;
border-radius:16px;
border-left:6px solid #1565c0;
background:#e3f2fd;
box-shadow:0 6px 18px rgba(0,0,0,0.06);
text-align:center;
height:150px;
display:flex;
flex-direction:column;
justify-content:center;
"""

card_style_blue_2 = """
padding:22px;
border-radius:16px;
border-left:6px solid #1565c0;
background:#e3f2fd;
box-shadow:0 6px 18px rgba(0,0,0,0.06);
text-align:center;
height:150px;
display:flex;
flex-direction:column;
justify-content:center;
"""

card_style_blue_3 = """
padding:22px;
border-radius:16px;
border-left:6px solid #1565c0;
background:#e3f2fd;
box-shadow:0 6px 18px rgba(0,0,0,0.06);
text-align:center;
height:150px;
display:flex;
flex-direction:column;
justify-content:center;
"""


with col1:
    st.markdown(f"""
    <div class="card-hover" style="{card_style_blue_1}">
        <h3 style="margin-top:10px; margin-bottom:6px;"> Students Analyzed</h3>
        <h2 style="margin-top:0;">1,200+</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card-hover" style="{card_style_blue_2}">
        <h3 style="margin-top:10px; margin-bottom:6px;"> Average Placement Rate</h3>
        <h2 style="margin-top:0;">78%</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card-hover" style="{card_style_blue_3}">
        <h3 style="margin-bottom:6px;"> Skills Tracked</h3>
        <h2 style="margin-top:0;">50+</h2>
    </div>
    """, unsafe_allow_html=True)


st.divider()

# ---------------- INPUT SECTION ----------------
left, right = st.columns([2,1])

card_style_neutral = """
padding:20px;
border-radius:16px;
background:white;
box-shadow:0 6px 18px rgba(0,0,0,0.05);
margin-bottom:10px;
height:120px;
display:flex;
flex-direction:column;
justify-content:center;
"""


with left:
    st.markdown(f"""
    <div class="card-hover" style="{card_style_neutral}">
        <h3 style="margin-bottom:6px;">Student Profile Input</h3>
        <p style="font-size:14px; color:#555;">
        Provide academic details and resume information for analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="card-hover" style="{card_style_neutral}">
        <h3 style="margin-bottom:6px;">Analysis Overview</h3>
        <p style="font-size:14px; color:#555;">
        Our AI analyzes resume-job match, skills, and placement readiness.
        </p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")

# ---------- DEMO BUTTONS ----------
st.markdown("""
<div class="card-hover" style="
background:white;
padding:16px;
border-radius:16px;
box-shadow:0 6px 20px rgba(0,0,0,0.05);
margin-bottom:10px;
text-align:center;
">
    <h3 style="margin:0;">Quick Demo Profiles</h3>
</div>
""", unsafe_allow_html=True)


demo1, demo2, demo3 = st.columns(3)

# ---------- DEMO RESUMES ----------
STRONG_RESUME = """
Computer Science student with strong Python, SQL, Machine Learning and Git skills.
Built 4 projects including ML prediction system and full stack web app.
Solved 350+ LeetCode DSA problems.
Completed internship at fintech startup improving API performance by 35%.
Participated in 3 hackathons and won 1st prize.
Strong communication and teamwork experience.
"""

AVERAGE_RESUME = """
Computer Science student with basic Python and SQL knowledge.
Built 2 academic projects including simple website and data analysis.
Solved 80 DSA problems.
Good communication skills and teamwork experience.
"""

WEAK_RESUME = """
Student learning programming.
Made one small project.
Looking for opportunities.
"""

STRONG_JD = """
Software Engineer role requiring Python, SQL, Git, Machine Learning,
Data Structures and communication skills.
Candidate should build scalable systems and analyze data.
"""

AVERAGE_JD = """
Backend Developer with Python, SQL and Git skills.
Good communication required.
"""

WEAK_JD = """
Any job.
"""


# ---------- MODIFY DEMO BUTTONS ----------
with demo1:
    if st.button("Strong Candidate"):
        st.session_state.cgpa = 8.8
        st.session_state.internship = 1
        st.session_state.projects = 4
        st.session_state.communication = 8
        st.session_state.dsa_score = 8
        st.session_state.hackathons = 3
        st.session_state.resume_demo = STRONG_RESUME
        st.session_state.jd_demo = STRONG_JD

with demo2:
    if st.button("Average Candidate"):
        st.session_state.cgpa = 7.2
        st.session_state.internship = 0
        st.session_state.projects = 2
        st.session_state.communication = 6
        st.session_state.dsa_score = 5
        st.session_state.hackathons = 1
        st.session_state.resume_demo = AVERAGE_RESUME
        st.session_state.jd_demo = AVERAGE_JD

with demo3:
    if st.button("Weak Candidate"):
        st.session_state.cgpa = 6.0
        st.session_state.internship = 0
        st.session_state.projects = 0
        st.session_state.communication = 4
        st.session_state.dsa_score = 2
        st.session_state.hackathons = 0
        st.session_state.resume_demo = WEAK_RESUME
        st.session_state.jd_demo = WEAK_JD


# ---------- DEFAULT VALUES ----------
if "cgpa" not in st.session_state:
    st.session_state.cgpa = 7.5
if "internship" not in st.session_state:
    st.session_state.internship = 0
if "projects" not in st.session_state:
    st.session_state.projects = 2
if "communication" not in st.session_state:
    st.session_state.communication = 6
if "dsa_score" not in st.session_state:
    st.session_state.dsa_score = 5
if "hackathons" not in st.session_state:
    st.session_state.hackathons = 1


# ---------- INPUT SLIDERS ----------
col1, col2 = st.columns(2)

with col1:
    cgpa = st.slider("CGPA", 5.0, 10.0, st.session_state.cgpa)
    internship = st.selectbox(
        "Internship Experience",
        [0, 1],
        index=st.session_state.internship
    )
    projects = st.slider("Number of Projects", 0, 5, st.session_state.projects)
    communication = st.slider(
        "Communication Skill (1-10)",
        1, 10,
        st.session_state.communication
    )
    dsa_score = st.slider(
        "DSA / Coding Skill (1-10)",
        1, 10,
        st.session_state.dsa_score
    )
    hackathons = st.slider(
        "Hackathons / Certifications",
        0, 5,
        st.session_state.hackathons
    )


# ---------- SAVE BACK ----------
st.session_state.cgpa = cgpa
st.session_state.internship = internship
st.session_state.projects = projects
st.session_state.communication = communication
st.session_state.dsa_score = dsa_score
st.session_state.hackathons = hackathons




with col2:
    role = st.selectbox(
    "Select Target Role",
    [
        "Custom",
        "Python Developer",
        "Data Analyst",
        "ML Engineer",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
        "Software Engineer",
        "Mechanical Engineer",
        "Cybersecurity Analyst",
        "DevOps Engineer",
        "Cloud Engineer",
        "Business Analyst",
        "QA Engineer",
        "AI Research Intern",
        "Mobile App Developer",
        "Database Engineer",
        "Product Engineer",
        "Robotics Engineer",
        "Data Scientist",
        "Amazon SDE",
        "Google SWE",
        "Infosys Graduate Engineer",
        "Startup Intern"
    ]
)
    role_difficulty = {
        # ---- Standard Roles ----
        "Python Developer": 0.95,
        "Backend Developer": 1.0,
        "Frontend Developer": 0.95,
        "Full Stack Developer": 1.05,
        "Software Engineer": 1.05,
        "Data Analyst": 1.0,
        "ML Engineer": 1.15,
        "Data Scientist": 1.2,
        "Cybersecurity Analyst": 1.1,
        "DevOps Engineer": 1.15,
        "Cloud Engineer": 1.1,
        "Database Engineer": 1.05,
        "QA Engineer": 0.9,
        "Business Analyst": 0.95,
        "Mobile App Developer": 1.0,
        "Product Engineer": 1.05,

        # ---- Core Engineering ----
        "Mechanical Engineer": 1.0,
        "Robotics Engineer": 1.2,
        "AI Research Intern": 1.25,

        # ---- Company Specific ----
        "Amazon SDE": 1.35,
        "Google SWE": 1.4,
        "Infosys Graduate Engineer": 0.9,
        "Startup Intern": 0.85,

        "Custom": 1.0
    }


    role_descriptions = {

        # -------- CORE ROLES --------

        "Python Developer":
        """
        We are hiring a Python Developer to build backend services and APIs.
        Required skills include Python, SQL, Git, data structures and communication.
        Experience with Flask/Django and debugging production issues preferred.
        """,

        "Data Analyst":
        """
        Looking for Data Analyst with Python, SQL, data analysis,
        data visualization and communication skills.
        Candidate must prepare dashboards, analyze trends,
        and present business insights.
        """,

        "ML Engineer":
        """
        Hiring ML Engineer experienced in Python, SQL,
        machine learning, data analysis, Git and communication.
        Candidate should build regression/classification models,
        evaluate performance and deploy models.
        """,

        "Backend Developer":
        """
        Backend Developer needed with Python or Java,
        SQL databases, Git, APIs, data structures and communication.
        Experience building scalable services and debugging systems required.
        """,

        "Frontend Developer":
        """
        Frontend Developer with HTML, CSS, JavaScript,
        Git and communication skills.
        Experience building responsive UI and integrating APIs preferred.
        """,

        "Full Stack Developer":
        """
        Full Stack Developer with Python/Java, HTML, CSS, SQL,
        Git and communication skills.
        Candidate must build end-to-end web applications and APIs.
        """,

        "Software Engineer":
        """
        Software Engineer role requiring data structures,
        Python or Java, Git, SQL and communication.
        Candidate must design algorithms and write optimized code.
        """,

        "Mechanical Engineer":
        """
        Mechanical Engineer with CAD, problem solving,
        project documentation and communication skills.
        Experience in design analysis and teamwork required.
        """,

        "Cybersecurity Analyst":
        """
        Cybersecurity Analyst with networking basics,
        Python scripting, Git and communication.
        Candidate must analyze vulnerabilities and monitor systems.
        """,

        # -------- NEW REALISTIC ROLES --------

        "DevOps Engineer":
        """
        DevOps Engineer with Python scripting, Git,
        SQL and communication skills.
        Candidate should understand CI/CD pipelines,
        automation, cloud deployment and debugging systems.
        """,

        "Cloud Engineer":
        """
        Cloud Engineer required with Python, Git,
        SQL and communication skills.
        Candidate must manage cloud deployments,
        monitor systems and automate workflows.
        """,

        "Business Analyst":
        """
        Business Analyst with communication,
        data analysis, SQL and reporting skills.
        Candidate should prepare dashboards,
        interpret data and present insights.
        """,

        "QA Engineer":
        """
        QA Engineer with Python scripting, Git,
        debugging and communication.
        Candidate must design test cases,
        perform automation testing and analyze defects.
        """,

        "AI Research Intern":
        """
        AI Research Intern with Python,
        machine learning, data analysis and communication.
        Candidate should implement algorithms,
        run experiments and document findings.
        """,

        "Mobile App Developer":
        """
        Mobile Developer with Java/Python backend,
        Git, APIs and communication skills.
        Candidate must build mobile apps and debug issues.
        """,

        "Database Engineer":
        """
        Database Engineer with strong SQL,
        data analysis, Python scripting,
        Git and communication skills.
        Candidate should design schemas and optimize queries.
        """,

        "Product Engineer":
        """
        Product Engineer with Python or Java,
        Git, SQL and communication skills.
        Candidate must build scalable features
        and collaborate across teams.
        """,

        "Robotics Engineer":
        """
        Robotics Engineer with Python,
        data analysis, problem solving and communication.
        Experience with sensor data and testing preferred.
        """,

        "Data Scientist":
        """
        Data Scientist with Python, SQL,
        machine learning, data analysis,
        Git and communication.
        Candidate must clean datasets,
        build predictive models and present insights.
        """,

        # -------- COMPANY-STYLE ROLES --------

        "Amazon SDE":
        """
        Amazon Software Development Engineer role requiring
        data structures, algorithms,
        Python or Java,
        SQL, Git and communication skills.
        Candidate must build scalable systems,
        write optimized code and participate in design reviews.
        """,

        "Google SWE":
        """
        Google Software Engineer role requiring strong
        problem solving, data structures,
        Python or Java,
        system design,
        Git and communication.
        Candidate must design efficient algorithms
        and collaborate in large codebases.
        """,

        "Infosys Graduate Engineer":
        """
        Graduate Engineer Trainee with Python or Java,
        SQL, Git and communication skills.
        Candidate must learn enterprise systems,
        debug issues and work in Agile teams.
        """,

        "Startup Intern":
        """
        Startup Intern with Python,
        data analysis,
        Git and communication skills.
        Candidate should build quick prototypes,
        debug features and collaborate in small teams.
        """
        }


    # ---------- Resume Input ----------
    st.markdown("### Resume Input")

    uploaded_file = st.file_uploader(
        "Upload your resume PDF",
        type=["pdf"],
        key="resume_pdf_upload"
    )

    extracted_text = ""

    if uploaded_file is not None:
        try:
            text_pages = []
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    txt = page.extract_text()
                    if txt:
                        text_pages.append(txt)

            extracted_text = "\n".join(text_pages)
            st.success(f"Uploaded: {uploaded_file.name}")

        except:
            st.error("Could not read this PDF. Try another resume.")

    # 🔹 Lock typing if PDF uploaded
    if extracted_text != "":
        resume_text = st.text_area(
            "Resume Text (from PDF)",
            extracted_text,
            height=200,
            disabled=True
        )
    else:
        resume_text = st.text_area(
        "Paste Resume Text",
        value=st.session_state.get("resume_demo", "")
    )



    if role == "Custom":
        job_description = st.text_area(
            "Paste Job Description",
            value=st.session_state.get("jd_demo", "")
        )

    else:
        job_description = role_descriptions[role]
        st.text_area("Job Description (Auto-filled)", job_description, disabled=True)

# ---------- SKILL TAG FUNCTION ----------
def show_tags(skills, color="#e8f4ff"):
    tag_html = ""
    for s in skills:
        tag_html += f"""
        <span style="
            background:{color};
            padding:6px 10px;
            border-radius:8px;
            margin:4px;
            display:inline-block;
            font-size:13px;">
            {s.title()}
        </span>
        """
    st.markdown(tag_html, unsafe_allow_html=True)

def show_tags(skills, color="#e8f4ff"):
    tag_html = ""
    for s in skills:
        tag_html += f'<span style="background:{color}; padding:6px 10px; border-radius:8px; margin:4px; display:inline-block;">{s.title()}</span>'
    st.markdown(tag_html, unsafe_allow_html=True)

      
# ---------------- ANALYZE ----------------
if st.button("Analyze"):

    # ---------- VALIDATION ----------
    if not resume_text.strip():
        st.error("Please paste resume text.")
        st.stop()

    if not job_description.strip():
        st.error("Please provide job description.")
        st.stop()
    
    with st.spinner("Analyzing profile..."):

        progress = st.progress(0)

        st.write("Extracting resume skills...")
        time.sleep(0.6)
        progress.progress(25)

        st.write("Matching with job description...")
        time.sleep(0.6)
        progress.progress(50)

        st.write("Running placement prediction model...")
        time.sleep(0.6)
        progress.progress(75)

        st.write("Generating improvement roadmap...")
        time.sleep(0.6)
        progress.progress(100)


        SKILLS = {
            "python": ["python"],
            "sql": ["sql"],
            "machine learning": ["machine learning", "ml"],
            "data analysis": ["data analysis", "analysis"],
            "git": ["git", "github"],
            "communication": ["communication", "presentation", "teamwork"],
        }

        resume_clean = resume_text.lower()
        job_clean = job_description.lower()

        resume_skills = []
        job_skills = []

        # ---------- SKILL DETECTION ----------
        for skill, keywords in SKILLS.items():
            if any(k in resume_clean for k in keywords):
                resume_skills.append(skill)
            if any(k in job_clean for k in keywords):
                job_skills.append(skill)

        # ---------- RESUME QUALITY ----------
        word_count = len(resume_text.split())
        numbers_found = sum(c.isdigit() for c in resume_text)

        resume_quality = (
            min(word_count / 200, 1) * 4 +           # good length
            min(len(resume_skills) / 6, 1) * 4 +     # skills richness
            min(numbers_found / 10, 1) * 2           # quantified achievements
        )

        resume_quality = round(resume_quality, 2)   # out of 10

        
        # ---- Resume Validation ----

        text = resume_text.strip()

        if text == "":
            st.error("Please paste your resume.")
            st.stop()

        words = text.lower().split()

        # garbage like "asdfgh"
        if len(words) <= 1:
            st.error("Resume text seems invalid.")
            st.stop()

        # repeated spam like "python python python"
        if len(set(words)) <= 1:
            st.error("Resume text looks like repeated spam.")
            st.stop()

        # few skills → just warn
        if len(resume_skills) == 0:
            st.warning("No recognizable technical skills found.")
        elif len(resume_skills) <= 2:
            st.info("Few skills detected. Consider adding more skills.")


        # ---------- SMART RESUME VALIDATION ----------
        text = resume_text.strip()

        if len(text) == 0:
            st.error("Please paste your resume.")
            st.stop()

        words = text.lower().split()
        real_words = [w for w in words if any(c.isalpha() for c in w)]

        if len(real_words) < 3:
            st.error("Resume text seems invalid.")
            st.stop()

        unique_ratio = len(set(words)) / max(len(words), 1)
        if len(words) > 6 and unique_ratio < 0.3:
            st.error("Resume text looks like repeated spam.")
            st.stop()

        match_percentage = 0
        if len(job_skills) > 0:
            match_percentage = round(
                (len(set(resume_skills).intersection(job_skills)) / len(job_skills)) * 100, 2
            )

        missing_skills = list(set(job_skills) - set(resume_skills))

        # ---------- MODEL ----------
        try:
            input_features = np.array([[
                cgpa,
                internship,
                communication,
                match_percentage
            ]])

            
        except:
            st.error("Prediction failed. Model mismatch.")
            st.stop()

        raw_prob = model.predict_proba(input_features)[0][1]

        # Base model weight
        probability = raw_prob * 60

        # ---------- EXTRA FACTORS ----------
        probability += projects * 1.2
        probability += dsa_score * 0.8
        probability += resume_quality * 0.7
        probability += hackathons * 0.6

        # Role difficulty
        probability *= role_difficulty.get(role, 1.0)

        # Penalties
        if internship == 0:
            probability *= 0.9

        if cgpa < 6.5:
            probability *= 0.85

        if match_percentage < 40:
            probability *= 0.8

        probability = max(5, min(probability, 95))
        probability = round(probability, 2)



        st.divider()
        st.markdown("""
            <style>
            .results-box {
                background: linear-gradient(90deg,#2563eb,#1e40af);
                color: white;
                padding: 14px 22px;
                border-radius: 14px;
                font-size: 28px;
                font-weight: 600;
                margin-top: 15px;
                margin-bottom: 15px;
                text-align: center;
                transition: all 0.25s ease;
            }

            .results-box:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 22px rgba(0,0,0,0.18);
                background: linear-gradient(90deg,#1e40af,#1e3a8a);
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown('<div class="results-box">Results</div>', unsafe_allow_html=True)


        colA, colB, colC = st.columns(3)

        metric_box = """
            height:140px;
            width:100%;
            padding:10px;
            border-radius:16px;
            box-shadow:0 4px 12px rgba(0,0,0,0.06);
            text-align:center;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
            transition:0.2s;
            """


        hover = """
        onmouseover="this.style.transform='scale(1.03)'"
        onmouseout="this.style.transform='scale(1)'"
        """

        with colA:
            st.markdown(f"""
            <div style="{metric_box}" {hover}>
                <h4>Match %</h4>
                <h2>{match_percentage}%</h2>
            </div>
            """, unsafe_allow_html=True)

        with colB:
            st.markdown(f"""
            <div style="{metric_box}" {hover}>
                <h4>Placement Probability</h4>
                <h2>{probability}%</h2>
            </div>
            """, unsafe_allow_html=True)

        with colC:
            st.markdown(f"""
            <div style="{metric_box}" {hover}>
                <h4>Matched Skills</h4>
                <h2>{len(resume_skills)}</h2>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.write(f"Resume Quality Score: {resume_quality}/10")

        # ---------- WHY THIS SCORE ----------
        st.subheader(" Why this score?")

        reasons = []

        if cgpa >= 8:
            reasons.append(f"Strong CGPA (+{round(cgpa*1.5,1)}%)")
        elif cgpa < 6.5:
            reasons.append("Low CGPA (-8%)")

        if internship == 1:
            reasons.append("Internship experience (+10%)")
        else:
            reasons.append("No internship (-10%)")

        if match_percentage >= 70:
            reasons.append(f"Good skill match (+{round(match_percentage/5,1)}%)")
        elif match_percentage < 40:
            reasons.append("Low skill match (-10%)")

        if communication >= 7:
            reasons.append("Good communication (+6%)")
        elif communication <= 4:
            reasons.append("Weak communication (-6%)")

        if dsa_score >= 7:
            reasons.append("Strong DSA skills (+8%)")
        elif dsa_score <= 3:
            reasons.append("Weak DSA skills (-8%)")

        if hackathons >= 2:
            reasons.append("Certifications/Hackathons (+5%)")

        if len(reasons) == 0:
            st.write("Balanced profile with no major strengths or weaknesses.")
        else:
            for r in reasons:
                st.write("•", r)


        st.caption("Prediction confidence derived from academic scores, internship exposure, skill alignment, coding strength, and resume quality metrics.")

        # ---------- Resume Strength Meter ----------
        st.subheader("📄 Resume Strength")

        st.progress(int(resume_quality * 10))

        if resume_quality < 4:
            st.warning("Resume needs major improvement.")
        elif resume_quality < 7:
            st.info("Resume is decent but can be improved.")
        else:
            st.success("Strong resume structure.")


        st.subheader(" Why This Score?")

        reasons = []

        if cgpa >= 8:
            reasons.append("Strong academic performance boosted your score.")
        elif cgpa < 6.5:
            reasons.append("Low CGPA reduced your placement chances.")

        if internship == 1:
            reasons.append("Internship experience increased industry readiness.")
        else:
            reasons.append("No internship experience lowered real-world exposure.")

        if match_percentage >= 70:
            reasons.append("Your skills match the job requirements well.")
        elif match_percentage < 40:
            reasons.append("Low skill match with job description reduced score.")

        if dsa_score >= 7:
            reasons.append("Strong DSA/problem solving is a big advantage.")
            
        if hackathons >= 2:
            reasons.append("Hackathons/certifications improved profile strength.")

        if resume_quality >= 7:
            reasons.append("Well-structured resume improved recruiter impression.")

        for r in reasons:
            st.write("•", r)



        st.write("Placement Readiness Score")
        st.markdown(f"""
            <div style="
            width:140px;
            height:140px;
            border-radius:50%;
            background:conic-gradient(#1f77b4 {probability}%, #eee {probability}%);
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:22px;
            margin:auto;">
            <b>{probability}%</b>
            </div>
            """, unsafe_allow_html=True)


        st.subheader("Skill Profile")
        skills_df = pd.DataFrame({
            "Category": ["CGPA", "Projects", "Skill Match", "Communication"],
            "Score": [cgpa*10, projects*20, match_percentage, communication*10]
        })
        st.bar_chart(skills_df.set_index("Category"))

        st.subheader(f"Missing Skills ({len(missing_skills)})")

        if missing_skills:
            for skill in missing_skills:
                st.write(f"• {skill.title()}")
        else:
            st.success("No major skill gaps detected.")

        if probability >= 80:
            st.success("High Placement Readiness")
        elif probability >= 50:
            st.warning("Moderate Placement Readiness")
        else:
            st.error("Low Placement Readiness - Improvement Required")

        st.divider()
        st.info(
            "This score reflects academic performance, project experience, "
            "skill alignment with job role, and communication ability."
        )

        # ---------- EXPLAINABILITY PANEL ----------
        st.divider()
        st.subheader(" Why This Score?")

        strengths = []
        improvements = []

        if cgpa >= 8:
            strengths.append("Strong CGPA")
        else:
            improvements.append("Improve academic performance")

        if internship == 1:
            strengths.append("Internship experience")
        else:
            improvements.append("Get internship experience")

        if match_percentage >= 70:
            strengths.append("Good skill match with job role")
        elif match_percentage >= 40:
            improvements.append("Improve skill match with job role")
        else:
            improvements.append("Major skill gaps for target role")

        if dsa_score >= 7:
            strengths.append("Good Dsa / Coding ability")
        else:
            improvements.append("Practice Dsa problems")

        if hackathons >= 2:
            strengths.append("Active in hackathons / certifications")
        else:
            improvements.append("Do certifications or hackathons")

        if resume_quality >= 7:
            strengths.append("Strong resume quality")
        else:
            improvements.append("Improve resume structure and achievements")

        st.markdown("### Strengths")
        for s in strengths:
            st.success(f"▸ {s}")

        st.markdown("### Needs Improvement")
        for i in improvements:
            st.warning(f"▸ {i}")

        # ---------- INSIGHT PANEL ----------
        st.divider()
        st.markdown(
        "<h3 style='text-align:center;'>Placement Insights</h3>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        box_style = """
        padding:18px;
        border-radius:14px;
        border:1px solid #e6eaf2;
        transition:0.2s;
        """

        hover_css = """
        <style>
        .box-hover:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        }
        </style>
        """
        st.markdown(hover_css, unsafe_allow_html=True)


        # ---------- STRENGTHS ----------
        with col1:

            strengths = []

            if cgpa >= 8:
                strengths.append("Strong academic performance")
            if internship == 1:
                strengths.append("Internship experience adds real-world exposure")
            if len(resume_skills) >= 4:
                strengths.append("Good skill coverage for the role")
            if dsa_score >= 7:
                strengths.append("Strong problem-solving ability")
            if hackathons >= 2:
                strengths.append("Active in hackathons / certifications")

            if not strengths:
                strengths.append("You're doing well — keep pushing forward 🚀")

            html = "<br>".join([f"• {s}" for s in strengths])

            st.markdown(
                f"""
                <div class='box-hover' style="{box_style}">
                    <h3>Strengths</h3>
                    {html}
                </div>
                """,
                unsafe_allow_html=True
            )


        # ---------- WEAK AREAS ----------
        with col2:

            weak = []

            if cgpa < 7:
                weak.append("Low CGPA may affect shortlist chances")
            if internship == 0:
                weak.append("No internship experience")
            if len(resume_skills) <= 2:
                weak.append("Limited technical skills detected")
            if match_percentage < 50:
                weak.append("Resume not aligned with job role")
            if dsa_score <= 5:
                weak.append("Improve coding/problem-solving skills")

            if not weak:
                weak.append("No major weak areas — keep growing 🔥")

            html = "<br>".join([f"• {w}" for w in weak])

            st.markdown(
                f"""
                <div class='box-hover' style="{box_style}; text-align:center;">
                    <h3>Weak Areas</h3>
                    {html}
                </div>
                """,
                unsafe_allow_html=True
            )


        
        st.subheader("Exact Next Steps")

        if match_percentage < 60:
            st.write("• Add missing skills from job description")

        if internship == 0:
            st.write("• Try 1–2 internships or open-source projects")

        if dsa_score < 7:
            st.write("• Solve 150+ DSA problems on LeetCode")

        if resume_quality < 6:
            st.write("• Add quantified achievements (numbers, impact)")

        if hackathons < 2:
            st.write("• Participate in hackathons or certifications")

        if cgpa < 7.5:
            st.write("• Focus on academics next semester")

        st.write("• Do mock interviews weekly")
        st.write("• Build 1 real-world project")
        

        st.subheader("Learning Roadmap")

        ROADMAP_LIBRARY = {
            "python": "Complete Python OOP and build 2 mini projects.",
            "sql": "Practice SQL joins and queries.",
            "machine learning": "Build one ML project.",
            "data analysis": "Learn Pandas + visualization.",
            "git": "Learn Git branching and maintain repo.",
            "communication": "Practice mock interviews.",
            "data structures": "Solve 100+ DSA problems."
        }

        if missing_skills:
            for skill in missing_skills:
                if skill in ROADMAP_LIBRARY:
                    st.write("•", ROADMAP_LIBRARY[skill])
        else:
            st.write("No major skill gaps. Focus on advanced projects.")
        
        # ---------- Recruiter Recommendation ----------
        st.subheader(" Recruiter Recommendation")

        if probability >= 85:
            st.success("Ready to apply to top product companies.")
        elif probability >= 65:
            st.info("Ready for mid-tier companies. Improve 1-2 skills for top companies.")
        else:
            st.warning("Focus on internships, DSA, and skill matching before applying.")

        # ---------- Company Readiness ----------
        st.subheader(" Company Readiness")

        company_targets = {
            "Amazon SDE": 1.2,
            "Google SWE": 1.25,
            "Infosys Graduate Engineer": 0.9,
            "Startup Intern": 0.8
        }

        for company, difficulty in company_targets.items():
            company_score = probability / difficulty
            company_score = round(max(5, min(company_score, 95)), 1)

            if company_score >= 85:
                st.success(f"{company} → {company_score}% Ready")
            elif company_score >= 65:
                st.info(f"{company} → {company_score}% Almost Ready")
            else:
                st.warning(f"{company} → {company_score}% Needs Improvement")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; font-size:14px;'>"
    "PlacementIQ • HackWave 2026 • Built with "
    "</p>",
    unsafe_allow_html=True
)





