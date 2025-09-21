import streamlit as st
from logic import evaluate_resume
import fitz  # PyMuPDF
import docx2txt

# --- File Readers ---
def getTextFromPDF(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def getTextFromDOCX(file):
    return docx2txt.process(file)

# --- Streamlit Config ---
st.set_page_config(
    page_title="Resume Relevance Checker",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS Styling with dynamic gradient ---
st.markdown(
    """
    <style>
    /* Background with animated gradient */
    .stApp {
        background: linear-gradient(135deg, #27476E 0%, #1F3A5A 50%, #27476E 100%);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
        color: #EAF8BF;
        font-family: 'Segoe UI', sans-serif;
    }

    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Title */
    h1 {
        text-align: center;
        font-weight: 900 !important;
        font-size: 2.5rem !important;
        background: -webkit-linear-gradient(#EAF8BF, #DFF2A5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }

    /* Subheaders */
    h2, h3, h4 {
        color: #EAF8BF !important;
        font-weight: 600 !important;
    }

    /* Card style with glassmorphism */
    .stMarkdown, .stTextArea, .stFileUploader, .stButton>button, .stAlert, .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(234,248,191,0.3);
        color: #EAF8BF;
        transition: 0.3s ease;
    }

    /* Button */
    .stButton>button {
        background: linear-gradient(90deg, #EAF8BF, #DFF2A5);
        border: none;
        color: #27476E;
        font-weight: 700;
        padding: 0.7rem 1.5rem;
        border-radius: 12px;
        width: 100%;
        cursor: pointer;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(234,248,191,0.6);
    }

    /* Metric Cards */
    .stMetric {
        text-align: center;
        background: rgba(234,248,191,0.1);
        border: 1px solid #EAF8BF;
        border-radius: 15px;
        padding: 20px;
        font-size: 1.2rem;
        font-weight: bold;
        color: #EAF8BF;
        transition: 0.3s ease;
    }

    /* Info Box */
    .stAlert {
        border-left: 5px solid #EAF8BF !important;
    }

    /* Center text */
    .center-text {
        text-align: center;
        color: #EAF8BF;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- Header ---
st.title("📄 Automated Resume Relevance Check System")
st.markdown(
    "<div class='center-text'>Upload a Job Description and Resume to get an instant relevance evaluation 🌿</div>",
    unsafe_allow_html=True,
)

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Job Description")
    jd_input = st.text_area("Paste JD here", height=250)

with col2:
    st.subheader("📂 Upload Resume")
    resume_file = st.file_uploader("Upload PDF/DOCX", type=["pdf", "docx"])

# --- Evaluate Button ---
if st.button("🔍 Evaluate Resume"):
    if jd_input and resume_file:
        # Extract resume text
        if resume_file.name.endswith(".pdf"):
            resume_text = getTextFromPDF(resume_file)
        else:
            resume_text = getTextFromDOCX(resume_file)

        # --- Minimum character check ---
        if len(resume_text.strip()) < 300:
            st.warning("⚠️ The uploaded resume is too short (<300 characters). Please provide a full resume for meaningful evaluation.")
        else:
            with st.spinner("🌿 Evaluating resume..."):
                result = evaluate_resume(jd_input, resume_text)

            # --- Results ---
            st.success("✅ Evaluation Complete!")
            st.metric("Final Relevance Score", f"{result['final_score']}%")
            st.write(f"**Verdict:** {result['verdict']}")

            st.subheader("📌 Skill Analysis")
            st.write(f"**✅ Found Skills:** {', '.join(result['found_skills'])}")
            st.write(f"**❌ Missing Skills:** {', '.join(result['missing_skills'])}")

            st.subheader("💡 Feedback")
            st.info(result["feedback"])

    else:
        st.warning("⚠️ Please provide both Job Description and Resume file.")
