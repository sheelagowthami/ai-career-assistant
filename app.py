import streamlit as st
import pandas as pd
import PyPDF2
from collections import Counter

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Career Assistant", page_icon="🤖")

st.title("🤖 AI Career Assistant")
st.write("Upload your resume and get career insights 🚀")

# -----------------------------
# LOAD DATASET
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("skills.csv")

data = load_data()

# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_text(file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    except:
        st.error("Error reading PDF file")
    return text.lower()

# -----------------------------
# SKILL EXTRACTION
# -----------------------------
def extract_skills(text):
    found_skills = []
    for skill in data['skill']:
        if skill.lower() in text:
            found_skills.append(skill)
    return list(set(found_skills))

# -----------------------------
# ROLE PREDICTION
# -----------------------------
def predict_role(skills):
    roles = []

    for skill in skills:
        role = data[data['skill'] == skill]['role'].values
        if len(role) > 0:
            roles.append(role[0])

    if roles:
        return Counter(roles).most_common(1)[0][0]
    else:
        return "Software Developer"

# -----------------------------
# SKILL RECOMMENDATION
# -----------------------------
def recommend_skills(role, user_skills):
    role_skills = data[data['role'] == role]['skill'].tolist()
    missing = list(set(role_skills) - set(user_skills))
    return missing

# -----------------------------
# RESUME SCORE (BONUS FEATURE)
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

if file is not None:
    st.success("Resume uploaded successfully ✅")

    # Extract text
    text = extract_text(file)

    # Extract skills
    skills = extract_skills(text)

    # Predict role
    role = predict_role(skills)

    # Recommend skills
    missing_skills = recommend_skills(role, skills)

    # Score
    score = calculate_score(skills, role)

    # -----------------------------
    # OUTPUT SECTION
    # -----------------------------
    st.subheader("🧠 Detected Skills")
    if skills:
        st.write(", ".join(skills))
    else:
        st.warning("No skills detected. Try a better resume.")

    st.subheader("💼 Suggested Career Role")
    st.success(role)

    st.subheader("📊 Resume Score")
    st.progress(score)
    st.write(f"Score: {score}/100")

    st.subheader("📈 Skills to Improve")
    if missing_skills:
        st.write(", ".join(missing_skills))
    else:
        st.success("Great! You already match this role well 🎯")

    st.subheader("🗺️ Learning Roadmap")
    if role == "AI Engineer":
        st.write("""
        • Learn Python deeply  
        • Study Machine Learning (Scikit-learn)  
        • Learn Deep Learning (TensorFlow/PyTorch)  
        • Build ML Projects  
        """)
    elif role == "Frontend Developer":
        st.write("""
        • Master HTML, CSS, JavaScript  
        • Learn React  
        • Build responsive websites  
        """)
    elif role == "Backend Developer":
        st.write("""
        • Learn Java/Python  
        • Study APIs & Databases  
        • Build backend projects  
        """)
    else:
        st.write("""
        • Learn Programming (Python/Java)  
        • Practice DSA  
        • Build projects  
        """)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
