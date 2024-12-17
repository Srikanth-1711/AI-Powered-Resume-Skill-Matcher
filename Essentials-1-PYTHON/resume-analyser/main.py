import PyPDF2
import docx
import re

def normalize_skills(skills):
    cleaned_skills = set()
    for skill in skills:
        skill = re.sub(r"\b(Basics of|Intermediate|Fundamentals of|Skills|Technical)\b", "", skill, flags=re.IGNORECASE).strip()
        skill = re.sub(r"&", ",", skill)
        cleaned_skills.update([s.strip().lower() for s in skill.split(",") if s.strip()])
    return cleaned_skills

def extract_text_from_file(file_path):
    text = ""
    try:
        if file_path.endswith(".pdf"):
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() if page.extract_text() else ""
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            print("Unsupported file format. Use PDF or DOCX.")
    except Exception as e:
        print(f"Error reading file: {e}")
    return text

resume_path = "S:\\Essentials-1-PYTHON\\Lakshmi_Srikanth_Polavarapu_Resume_NCR_Atleos.pdf"
job_desc_path = "S:\\Essentials-1-PYTHON\\JD-1.txt"

extracted_text = extract_text_from_file(resume_path)
print("Extracted Resume Text:\n", extracted_text)

def extract_sections(resume_text):
    sections = {"skills": [], "experience": [], "education": []}
    skills_match = re.search(r"(Skills|Technical Skills|Key Skills|Core Competencies)\s*[:\-]?\s*([\s\S]+?)(Experience|Education|Projects|$)", resume_text, re.IGNORECASE)
    if skills_match:
        sections["skills"] = skills_match.group(2).strip().split(", ")
    exp_match = re.search(r"(Experience|Work Experience)\s*[:\-]?\s*([\s\S]+?)(Skills|Education|Projects|$)", resume_text, re.IGNORECASE)
    if exp_match:
        sections["experience"] = exp_match.group(2).strip().split("\n")
    edu_match = re.search(r"(Education|Academic Background)\s*[:\-]?\s*([\s\S]+?)(Skills|Experience|Projects|$)", resume_text, re.IGNORECASE)
    if edu_match:
        sections["education"] = edu_match.group(2).strip().split("\n")
    return sections

sections = extract_sections(extracted_text)
print("Extracted Skills:", sections["skills"])
print("Extracted Experience:", sections["experience"])
print("Extracted Education:", sections["education"])

normalized_resume_skills = normalize_skills(sections["skills"])

def match_skills(resume_skills, job_description_path):
    try:
        with open(job_description_path, "r") as file:
            job_skills = set(file.read().split(":")[1].strip().split(", "))
        normalized_job_skills = normalize_skills(job_skills)
        matched_skills = resume_skills.intersection(normalized_job_skills)
        match_percentage = (len(matched_skills) / len(normalized_job_skills)) * 100
        return matched_skills, match_percentage
    except Exception as e:
        print(f"Error matching skills: {e}")
        return set(), 0.0

matched_skills, match_percent = match_skills(normalized_resume_skills, job_desc_path)

print("Matched Skills:", matched_skills)
print(f"Skill Match Percentage: {match_percent:.2f}%")

def generate_report(resume_path, matched_skills, match_percentage):
    print("\n--- Resume Analysis Report ---")
    print(f"File: {resume_path}")
    print("Matched Skills:", matched_skills)
    print(f"Skill Match Percentage: {match_percentage:.2f}%")
    print("--- End of Report ---")

generate_report(resume_path, matched_skills, match_percent)
