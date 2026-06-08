import pandas as pd

skills = pd.read_csv("data/skills.csv", header=None)[0].tolist()

def extract_skills(text):

    found_skills = []

    for skill in skills:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills