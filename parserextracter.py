import pdfplumber
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_details(text):
    doc = nlp(text)

    name = ""
    skills = []
    education = []
    email = ""
    phone = ""

    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
        elif ent.label_ in ["ORG", "EDUCATION"]:
            education.append(ent.text)

    # Regex-based
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if email_match:
        email = email_match.group(0)

    phone_match = re.search(r'\+?\d[\d\s\-]{8,}\d', text)
    if phone_match:
        phone = phone_match.group(0)

    # Extract simple skill list
    keywords = ['python', 'java', 'c++', 'sql', 'flask', 'django', 'excel', 'javascript', 'react']
    lower_text = text.lower()
    skills = list(set([kw for kw in keywords if kw in lower_text]))

    return {
        "name": name.strip(),
        "email": email,
        "phone": phone,
        "skills": ', '.join(skills),
        "education": '; '.join(set(education))
    }
