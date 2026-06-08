from groq import Groq
import streamlit as st

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

def recommend_courses(
    resume_text,
    missing_skills,
    job_description
):

    prompt = f"""
    You are an expert career mentor.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Missing Skills:
    {', '.join(missing_skills)}

    Analyze the candidate and provide:

    1. Recommended Courses
    2. Recommended Certifications
    3. Project Ideas
    4. Learning Roadmap
    5. Interview Preparation Topics

    Format nicely using headings and bullet points.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an expert career mentor."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content