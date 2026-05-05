import streamlit as st
import pandas as pd
import PyPDF2
from collections import Counter
import re

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Career Assistant", page_icon="🤖")
st.title("🤖 AI Career Assistant")
st.write("Upload your resume and get smart career insights 🚀")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("skills.csv")

data = load_data()

# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text

# -----------------------------
# EXTRACT TEXT FROM PDF
# -----------------------------
def extract_text(file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    except:
        st.error("Error reading PDF")
    return clean_text(text)

# -----------------------------
# EXTRACT SKILLS (IMPROVED)
# -----------------------------
def extract_skills(text):
    found_skills = []

    for skill in data['skill']:
        if skill.lower() in text:
            found_skills.append(skill.lower())

    return list(set(found_skills))

# -----------------------------
# ROLE SCORING (MAIN FIX 🔥)
# -----------------------------
def predict_role(skills):
    role_scores = {}

    for skill in skills:
        roles = data[data['skill'] == skill]['role'].values
        for role in roles:
            role_scores[role] = role_scores.get(role, 0) + 1

    if role_scores:
        best_role = max(role_scores, key=role_scores.get)
        return best_role, role_scores
    else:
        return "Software Developer", {}

# -----------------------------
# RECOMMEND SKILLS
# -----------------------------
def recommend_skills(role, user_skills):
    role_skills = data[data['role'] == role]['skill'].tolist()
    missing = list(set(role_skills) - set(user_skills))
    return missing

# -----------------------------
# SCORE CALCULATION
# -----------------------------
def calculate_score(user_skills, role):
    role_skills = data[data['role'] == role]['skill'].tolist()
    if len(role_skills) == 0:
        return 50

    score = (len(user_skills) / len(role_skills)) * 100
    return min(int(score), 100)

# -----------------------------
# FILE UPLOAD
# -----------------------------
file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")

if file:
    st.success("Resume uploaded successfully ✅")

    text = extract_text(file)
    skills = extract_skills(text)

    role, role_scores = predict_role(skills)
    missing = recommend_skills(role, skills)
    score = calculate_score(skills, role)

    # -----------------------------
    # OUTPUT
    # -----------------------------
    st.subheader("🧠 Detected Skills")
    if skills:
        st.write(", ".join(skills))
    else:
        st.warning("No skills detected")

    st.subheader("📊 Role Matching Scores")
    if role_scores:
        st.write(role_scores)

    st.subheader("💼 Suggested Role")
    st.success(role)

    st.subheader("📈 Resume Score")
    st.progress(score)
    st.write(f"{score}/100")

    st.subheader("📚 Skills to Improve")
    if missing:
        st.write(", ".join(missing))
    else:
        st.success("You match this role well 🎯")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
