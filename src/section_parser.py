def extract_sections(text):

    sections = {
        "skills": "",
        "projects": "",
        "experience": "",
        "education": "",
        "certifications": ""
    }

    lines = text.split('\n')

    current_section = None

    for line in lines:

        lower = line.lower()

        if "technical skills" in lower:
            current_section = "skills"

        elif "projects" in lower:
            current_section = "projects"

        elif "internship" in lower or "experience" in lower:
            current_section = "experience"

        elif "education" in lower:
            current_section = "education"

        elif "certifications" in lower:
            current_section = "certifications"

        elif current_section:
            sections[current_section] += line + " "

    return sections