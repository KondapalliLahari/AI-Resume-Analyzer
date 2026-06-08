                                                    AI Resume Analyzer
Overview

    AI Resume Analyzer is an intelligent web application that helps job seekers evaluate their resumes against a given Job Description (JD). The system analyzes resume content, calculates ATS (Applicant Tracking System) compatibility, identifies skill gaps, recommends learning resources, and provides AI-powered career guidance.

The project is built using Python, Streamlit, Natural Language Processing (NLP), and Large Language Models (LLMs).

Features
📄 Resume Analysis
    Upload resume in PDF format
    Extract resume text automatically
    Parse resume sections such as:
    Education
    Skills
    Projects
    Experience
    Certifications
📈 ATS Score Analysis
    Calculate overall ATS score
    Section-wise evaluation:
    Skills Match
    Project Relevance
    Experience Relevance
    Certification Relevance
    Interactive ATS score breakdown chart
🎯 Skill Gap Analysis
    Identify matched skills
    Detect missing skills required for the target role
    Calculate overall skill gap percentage
    Visual skill chips for easy understanding
📚 AI Course Recommendations
    Generate personalized course recommendations
    Analyze:
    Current resume skills
    Missing skills
    Job description requirements
    Suggest learning paths to improve employability
🤖 AI Career Assistant
    Interactive chatbot powered by LLM
    Career guidance and interview preparation
    Resume improvement suggestions
    Skill development recommendations
📄 Professional PDF Report

Generated report includes:

    ATS Score
    Skill Gap Analysis
    ATS Score Breakdown Chart
    Matched Skills
    Missing Skills
    Recommendations
    Strengths & Weaknesses
    Executive Summary
    Report Generation Timestamp
Tech Stack
    Frontend
        Streamlit
    Backend
        Python
    AI & NLP
        Groq API
        LLaMA 3.3 70B Versatile
        Semantic Similarity Matching
        NLP-based Skill Extraction
    Data Visualization
        Plotly
        Matplotlib
        Pandas
    PDF Generation
        ReportLab
Project Workflow
User uploads a resume.
    Resume text is extracted and cleaned.
    Skills and resume sections are identified.
    Job Description is analyzed.
    Semantic matching compares resume skills with job requirements.
    ATS score is calculated.
    Skill gaps are identified.
    Personalized course recommendations are generated.
    AI Career Assistant provides career guidance.
    Detailed PDF report is generated.
Folder Structure
AI-Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── .env
│
├── src/
│   ├── parser.py
│   ├── preprocess.py
│   ├── skills.py
│   ├── semantic_matcher.py
│   ├── section_parser.py
│   ├── advanced_matcher.py
│   ├── chatbot.py
│   └── course_recommender.py
│
├── assets/
├── reports/
└── README.md
Installation
Clone Repository
git clone https://github.com/yourusername/AI-Resume-Analyzer.git

cd AI-Resume-Analyzer
Install Dependencies
    pip install -r requirements.txt
Configure Environment Variables

Create a .env file:

GROQ_API_KEY=your_api_key_here

Run Application
streamlit run app.py

Future Enhancements
    Multi-format resume support (DOCX, TXT)
    Resume ranking against multiple job descriptions
    AI-generated resume rewriting
    Interview question generation
    Resume keyword optimization
    LinkedIn profile analysis
    Industry-specific ATS scoring
