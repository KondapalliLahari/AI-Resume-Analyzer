import streamlit as st
import tempfile
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from textwrap import wrap

from src.parser import extract_text_from_pdf
from src.preprocess import clean_text
from src.skills import extract_skills
from src.semantic_matcher import semantic_similarity
from src.section_parser import extract_sections
from src.advanced_matcher import (
    section_similarity,
    calculate_final_ats_score
)

def generate_pdf(
    final_score,
    skills_score,
    project_score,
    experience_score,
    certification_score,
    skill_gap,
    matched_skills,
    missing_skills,
    recommendations,
    strengths,
    weaknesses,
):

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    # Title
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(
        50,
        800,
        "AI Resume Analyzer Report"
    )

    pdf.setFont("Helvetica", 12)

    y = 760

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        50,
        780,
        f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
    )

    # ATS Scores
    pdf.drawString(
        50,
        y,
        f"Final ATS Score: {final_score}%"
    )
    y -= 25

    pdf.drawString(
        50,
        y,
        f"Skills Match: {skills_score}%"
    )
    y -= 20

    pdf.drawString(
        50,
        y,
        f"Projects Relevance: {project_score}%"
    )
    y -= 20

    pdf.drawString(
        50,
        y,
        f"Experience Relevance: {experience_score}%"
    )
    y -= 20

    pdf.drawString(
        50,
        y,
        f"Certification Relevance: {certification_score}%"
    )

    y -= 40

     #skill gap
    pdf.drawString(
        50,
        y,
        f"Skill Gap: {skill_gap}%"
    )

    y -= 30
    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(
        50,
        y,
        "Score Breakdown"
    )

    y -= 30

    scores = [
        ["Skills", skills_score],
        ["Projects", project_score],
        ["Experience", experience_score],
        ["Certifications", certification_score]
    ]

    pdf.setFont("Helvetica", 12)

    for item, score in scores:

        pdf.drawString(
            60,
            y,
            item
        )

        pdf.drawString(
            250,
            y,
            f"{score}%"
        )

        y -= 20

    y -= 20

    # Create chart image

    plt.figure(figsize=(6,4))

    plt.bar(
        ["Skills", "Projects", "Experience", "Certifications"],
        [
            skills_score,
            project_score,
            experience_score,
            certification_score
        ]
    )

    plt.ylabel("Score (%)")
    plt.title("ATS Score Breakdown")

    plt.savefig(
        "ats_chart.png",
        bbox_inches="tight"
    )

    plt.close()
    if y < 300:
        pdf.showPage()
        y = 800

    pdf.drawImage(
        "ats_chart.png",
        50,
        y - 220,
        width=450,
        height=220
    )

    y -= 250

    import os

    if os.path.exists("ats_chart.png"):
        os.remove("ats_chart.png")

    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(
        50,
        y,
        "Executive Summary"
    )

    y -= 25

    pdf.setFont("Helvetica", 11)

    summary = f"""
    The resume achieved an ATS score of {final_score}%.
    A total of {len(matched_skills)} skills matched the
    job description while {len(missing_skills)} skills
    were identified as missing. The skill gap is
    {skill_gap}%.
    """

    for line in wrap(summary, width=80):

        pdf.drawString(
            70,
            y,
            line
        )

        y -= 18
    # Matched Skills
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(
        50,
        y,
        "Matched Skills"
    )

    y -= 25

    pdf.setFont("Helvetica", 11)

    for skill in matched_skills:

        if y < 50:
            pdf.showPage()
            y = 800

        pdf.drawString(
            70,
            y,
            f"• {skill}"
        )

        y -= 18

    y -= 20

    # Missing Skills
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(
        50,
        y,
        "Missing Skills"
    )

    y -= 25

    pdf.setFont("Helvetica", 11)

    for skill in missing_skills:

        if y < 50:
            pdf.showPage()
            y = 800

        pdf.drawString(
            70,
            y,
            f"• {skill}"
        )

        y -= 18

    y -= 20

        # Recommendations
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(
        50,
        y,
        "Recommendations"
    )

    y -= 25

    pdf.setFont("Helvetica", 11)

    for rec in recommendations:

        lines = wrap(rec, width=80)

        for line in lines:

            pdf.drawString(
                70,
                y,
                f"• {line}"
            )

            y -= 18

            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 11)
                y = 800
    # Strengths Section
    if y < 100:
        pdf.showPage()
        y = 800

    y -= 20

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(
        50,
        y,
        "Strengths"
    )

    y -= 25

    pdf.setFont("Helvetica", 11)

    for item in strengths:

        lines = wrap(item, width=80)

        for line in lines:

            pdf.drawString(
                70,
                y,
                f"• {line}"
            )

            y -= 18

            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 11)
                y = 800

    # Weaknesses Section
    if y < 100:
        pdf.showPage()
        y = 800

    y -= 20


    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(
    50,
    y,
    "Weaknesses"
    )

    y -= 25

    pdf.setFont("Helvetica", 11)

    for item in weaknesses:

        lines = wrap(item, width=80)

        for line in lines:

            pdf.drawString(
                70,
                y,
                f"• {line}"
            )

            y -= 18

            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 11)
                y = 800

    pdf.save()

    buffer.seek(0)

    return buffer

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:

    st.markdown("""
    <h2 style='color:white; text-align:center;'>
        AI Resume Analyzer
    </h2>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "",
        [
            "Dashboard",
            "Resume Analysis",
            "ATS Score",
            "Skill Gap Analysis",
            "Course Recommendations",
            "AI Career Assistant",
            "Download Report"
        ]
    )

st.markdown("""
<style>

[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #001845,
        #023e8a,
        #0077ff,
        #00b4ff
    );
}
[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        135deg,
        #ffffff,
        #f0f9ff,
        #dbeafe,
        #bfdbfe
    );
}


[data-testid="stSidebar"] *{
    color:white;
}

div[role="radiogroup"] label{
    padding:12px;
    margin-bottom:8px;
    border-radius:10px;
}

div[role="radiogroup"] label:hover{
    background:#16355f;
}
.metric-card{
    background:#ffffff;
    border-radius:20px;
    padding:25px;
    text-align:center;
    margin:10px;
    min-height:170px;

    border:3px solid #ddd;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.12);
}

.ats-card{
    border:2px solid #3b82f6;
}

.match-card{
    border:2px solid #22c55e;
}

.missing-card{
    border:2px solid #f97316;
}

.gap-card{
    border:2px solid #8b5cf6;
}

.metric-value{
    font-size:42px;
    font-weight:bold;
    margin-top:15px;
    color:#111827;
}

.metric-title{
    font-size:18px;
    font-weight:700;
    color:#374151;
}
.skill-chip{
    display:inline-block;
    padding:10px 18px;
    margin:6px;
    border-radius:25px;
    font-weight:600;
    font-size:16px;
}

.matched-chip{
    background:#d1fae5;
    color:#065f46;
    border:2px solid #10b981;
}

.missing-chip{
    background:#fee2e2;
    color:#991b1b;
    border:2px solid #ef4444;
}

</style>
""", unsafe_allow_html=True)

def analyze_resume(uploaded_file, job_description):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp_file:

        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    resume_text = extract_text_from_pdf(temp_path)

    cleaned_resume = clean_text(resume_text)

    sections = extract_sections(resume_text)

    resume_skills = extract_skills(cleaned_resume)

    cleaned_jd = clean_text(job_description)

    job_skills = extract_skills(cleaned_jd)

    matched_skills, missing_skills = semantic_similarity(
        resume_skills,
        job_skills
    )

    if len(job_skills) > 0:
        skills_score = (
            len(matched_skills)
            / len(job_skills)
        ) * 100
    else:
        skills_score = 0

    projects_text = sections["projects"]
    experience_text = sections["experience"]
    cert_text = sections["certifications"]

    project_score = section_similarity(
        projects_text,
        job_description
    )

    experience_score = section_similarity(
        experience_text,
        job_description
    )

    certification_score = section_similarity(
        cert_text,
        job_description
    )

    resume_quality_score = 0

    if "github" in resume_text.lower():
        resume_quality_score += 20

    if "linkedin" in resume_text.lower():
        resume_quality_score += 20

    if len(resume_skills) >= 5:
        resume_quality_score += 20

    if len(projects_text.strip()) > 20:
        resume_quality_score += 20

    if len(experience_text.strip()) > 20:
        resume_quality_score += 20

    final_score = round(
        calculate_final_ats_score(
            skills_score,
            project_score,
            experience_score,
            certification_score,
            resume_quality_score
        ),
        2
    )

    if len(job_skills) > 0:
        skill_gap = round(
            (len(missing_skills) / len(job_skills)) * 100,
            2
        )
    else:
        skill_gap = 0

    return {
    "final_score": final_score,
    "skills_score": skills_score,
    "project_score": project_score,
    "experience_score": experience_score,
    "certification_score": certification_score,
    "skill_gap": skill_gap,
    "matched_skills": matched_skills,
    "missing_skills": missing_skills,
    "resume_text": resume_text,
    "sections": sections
}

# =========================
# DASHBOARD
# =========================

if menu == "Dashboard":

    st.title("📊 Dashboard")
    st.markdown("""
        <h3 style="
        color:#2563eb;
        font-size:22px;
        margin-bottom:30px;
        ">
        Resume Performance Overview
        </h3>
        """, unsafe_allow_html=True)
    if "results" in st.session_state:

        results = st.session_state["results"]
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card ats-card">
                <div class="metric-title">📊 ATS Score</div>
                <div class="metric-value">{results['final_score']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card match-card">
                <div class="metric-title">✅ Matched Skills</div>
                <div class="metric-value">{len(results['matched_skills'])}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card missing-card">
                <div class="metric-title">⚠️ Missing Skills</div>
                <div class="metric-value">{len(results['missing_skills'])}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card gap-card">
                <div class="metric-title">🎯 Skill Gap</div>
                <div class="metric-value">{results['skill_gap']}%</div>
            </div>
            """, unsafe_allow_html=True)
    else:

        st.info(
            "Analyze a resume first."
        )


# =========================
# RESUME ANALYSIS
# =========================

elif menu == "Resume Analysis":

    st.title("📄 Resume Analysis")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

    job_description = st.text_area(
        "Enter Job Description"
    )

    if st.button("Analyze Resume"):
        if uploaded_file is None:
            st.error("Upload resume first")
            st.stop()

        if not job_description.strip():
            st.error("Enter job description")
            st.stop()

        results = analyze_resume(
            uploaded_file,
            job_description
        )
        st.session_state["results"] = results

        st.session_state["job_description"] = job_description
        st.session_state["resume_skills"] = results["matched_skills"] + results["missing_skills"]
        st.session_state["job_skills"] = extract_skills(
            clean_text(job_description)
        )

        st.success(
            "Analysis completed successfully."
        )

        
# =========================
# ATS SCORE
# =========================

elif menu == "ATS Score":

    st.title("📈 ATS Score")

    if "results" not in st.session_state:
        st.warning("Analyze a resume first.")
        st.stop()

    results = st.session_state["results"]

    st.markdown(f"""
<div class="metric-card ats-card">
    <div class="metric-title">📈 Final ATS Score</div>
    <div class="metric-value">{results['final_score']}%</div>
</div>
""", unsafe_allow_html=True)

    score_df = pd.DataFrame({
    "Category": [
        "Skills",
        "Projects",
        "Experience",
        "Certifications"
    ],
    "Score": [
        round(results["skills_score"], 2),
        round(results["project_score"], 2),
        round(results["experience_score"], 2),
        round(results["certification_score"], 2)
    ]
})

    fig = px.bar(
        score_df,
        x="Category",
        y="Score",
        color="Category",
        text="Score",
        title="ATS Score Breakdown"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_range=[0, 100]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================
# SKILL GAP
# =========================

elif menu == "Skill Gap Analysis":

    st.title("🎯 Skill Gap Analysis")

    if "results" not in st.session_state:
        st.warning("Analyze a resume first.")
        st.stop()

    results = st.session_state["results"]

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("## ✅ Matched Skills")

        matched_html = ""

        for skill in results["matched_skills"]:
            matched_html += f"""
            <span class="skill-chip matched-chip">
                {skill.title()}
            </span>
            """

        st.markdown(matched_html, unsafe_allow_html=True)

    with col2:

        st.markdown("## ❌ Missing Skills")

        missing_html = ""

        for skill in results["missing_skills"]:
            missing_html += f"""
            <span class="skill-chip missing-chip">
                {skill.title()}
            </span>
            """

        st.markdown(missing_html, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown(f"""
        <div class="metric-card gap-card">
            <div class="metric-title">🎯 Skill Gap</div>
            <div class="metric-value">{results['skill_gap']:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)


# =========================
# COURSES
# =========================


elif menu == "Course Recommendations":

    st.title("📚 AI Course Recommendations")

    if "results" not in st.session_state:
        st.warning("Analyze a resume first.")
        st.stop()

    if st.button("Generate AI Recommendations"):

        from src.course_recommender import recommend_courses

        response = recommend_courses(
            st.session_state["results"]["resume_text"],
            st.session_state["results"]["missing_skills"],
            st.session_state["job_description"]
        )
        st.session_state["ai_recommendations"] = response

        st.markdown(response)


# =========================
# AI CHATBOT
# =========================

elif menu == "AI Career Assistant":

    st.title("🤖 AI Career Assistant")

    question = st.text_input(
        "Ask Career Question"
    )

    if st.button("Ask AI"):

        from src.chatbot import ask_ai

        answer = ask_ai(question)

        st.write(answer)


# =========================
# PDF DOWNLOAD
# =========================

elif menu == "Download Report":

    st.title("📄 Download Report")

    if "results" not in st.session_state:
        st.warning("Analyze a resume first.")
        st.stop()

    results = st.session_state["results"]

    recommendations = []

    for skill in results["missing_skills"]:

        recommendations.append(
            f"Consider learning {skill} through projects, certifications, or online courses."
        )

    strengths = []

    if results["skills_score"] >= 70:
        strengths.append(
            "Strong alignment of technical skills."
        )

    if len(results["matched_skills"]) >= 5:
        strengths.append(
            "Good number of required skills matched."
        )

    if results["experience_score"] >= 60:
        strengths.append(
            "Experience section is relevant."
        )

    weaknesses = [
        f"Missing {skill}"
        for skill in results["missing_skills"]
    ]

    pdf_file = generate_pdf(
        results["final_score"],
        results["skills_score"],
        results["project_score"],
        results["experience_score"],
        results["certification_score"],
        results["skill_gap"],
        results["matched_skills"],
        results["missing_skills"],
        recommendations,
        strengths,
        weaknesses,
    )

    st.download_button(
        label="📄 Download ATS Report",
        data=pdf_file,
        file_name="ATS_Report.pdf",
        mime="application/pdf"
    )
