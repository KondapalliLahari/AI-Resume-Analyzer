from matcher import calculate_similarity

cleaned = """
python sql machine learning pandas data visualization
"""

job_description = """
Looking for Python, SQL, Machine Learning,
Pandas, and Data Visualization skills.
"""

score = calculate_similarity(cleaned, job_description)

print(score)