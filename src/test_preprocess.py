from parser import extract_text_from_pdf
from preprocess import clean_text

text = extract_text_from_pdf("../data/resumes/komali-resume.pdf")

cleaned = clean_text(text)

print(cleaned)