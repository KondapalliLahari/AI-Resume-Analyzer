from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(resume_skills, job_skills):

    matched_skills = []
    missing_skills = []

    for job_skill in job_skills:

        job_embedding = model.encode([job_skill])

        found = False

        for resume_skill in resume_skills:

            resume_embedding = model.encode([resume_skill])

            similarity = cosine_similarity(
                job_embedding,
                resume_embedding
            )[0][0]

            if similarity > 0.6:
                matched_skills.append(job_skill)
                found = True
                break

        if not found:
            missing_skills.append(job_skill)

    return matched_skills, missing_skills