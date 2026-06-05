import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🚀 AI Resume Analyzer Dashboard")
st.markdown("### Smart ATS + Job Matching System")

# ================= UPLOAD =================
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

resume_text = ""

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

    st.success("Resume Loaded Successfully!")

# ================= SKILL MAP =================
skill_map = {
    "python": ["python", "programming"],
    "java": ["java"],
    "c++": ["c++"],
    "sql": ["sql", "database"],
    "machine learning": ["machine learning", "ai"],
    "html": ["html"],
    "css": ["css"],
    "javascript": ["javascript"],
    "communication": ["communication"],
    "teamwork": ["team"]
}

found_skills = []

# ================= ANALYSIS =================
if resume_text:

    text = resume_text.lower()

    for skill, keywords in skill_map.items():
        for key in keywords:
            if key in text:
                found_skills.append(skill)
                break

    found_skills = list(set(found_skills))

    score = (len(found_skills) / len(skill_map)) * 100

    missing_skills = [s for s in skill_map if s not in found_skills]

    status = (
        "Excellent 🎉" if score > 75 else
        "Good 👍" if score > 50 else
        "Needs Improvement ⚠️"
    )

    # ================= DASHBOARD =================
    col1, col2, col3 = st.columns(3)

    col1.metric("📊 ATS Score", f"{int(score)}%")
    col2.metric("🧠 Skills Found", len(found_skills))
    col3.metric("🎯 Status", status)

    # ================= TEXT =================
    st.subheader("📄 Resume Text")
    st.write(resume_text)

    st.subheader("🧠 Skills Found")
    st.write(found_skills)

    st.subheader("📉 Missing Skills")
    st.write(missing_skills)

    # ================= GRAPH =================
    st.subheader("📊 Skill Analysis Chart")

    if found_skills:
        fig, ax = plt.subplots()
        ax.bar(found_skills, [10]*len(found_skills))
        st.pyplot(fig)

    # ================= JOB MATCHING =================
    st.subheader("💼 Job Suggestions")

    job_map = {
        "python": "Software Developer",
        "machine learning": "Data Scientist",
        "sql": "Backend Developer",
        "html": "Frontend Developer"
    }

    for skill in found_skills:
        if skill in job_map:
            st.write(f"👉 You can apply for: **{job_map[skill]}**")

    # ================= PDF REPORT =================
    def generate_pdf():
        c = canvas.Canvas("resume_report.pdf")
        c.drawString(100, 800, f"ATS Score: {int(score)}%")
        c.drawString(100, 780, f"Skills: {', '.join(found_skills)}")
        c.save()

    generate_pdf()

    with open("resume_report.pdf", "rb") as f:
        st.download_button("📥 Download Report", f, file_name="resume_report.pdf")

    # ================= FINAL RESULT =================
    st.subheader("🏁 Final Result")

    if score > 75:
        st.success("Excellent Resume 🎉")
    elif score > 50:
        st.warning("Good Resume 👍")
    else:
        st.error("Needs Improvement ⚠️")

else:
    st.info("📌 Please upload a resume PDF to start analysis")
