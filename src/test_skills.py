from parser import extract_text_from_pdf
from preprocess import clean_text
from skills import extract_skills

# Extract resume text
text = extract_text_from_pdf("../data/resumes/lahari_resume.pdf")

# Clean text
cleaned = clean_text(text)

# Extract skills
print(extract_skills(cleaned))