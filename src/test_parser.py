from parser import extract_text_from_pdf

text = extract_text_from_pdf(
    r"C:\Users\lahar\OneDrive\Desktop\AI-Resume-Analyzer\data\resumes\lahari_resume.pdf"
)

print(text)