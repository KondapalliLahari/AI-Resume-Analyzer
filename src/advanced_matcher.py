from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def section_similarity(section_text, job_description):

    if not section_text.strip():
        return 0

    embeddings = model.encode(
        [section_text, job_description]
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(round(similarity * 100, 2))


def calculate_final_ats_score(
    skills_score,
    project_score,
    experience_score,
    certification_score,
    resume_quality_score
):

    final_score = (
        (skills_score * 0.35)
        + (project_score * 0.25)
        + (experience_score * 0.20)
        + (certification_score * 0.10)
        + (resume_quality_score * 0.10)
    )

    return round(final_score, 2)