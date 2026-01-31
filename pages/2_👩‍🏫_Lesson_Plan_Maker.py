import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Lesson Plan Maker", page_icon="👩‍🏫")

st.title("👩‍🏫 Lesson Plan Assistant")
st.write("Create a DepEd-style Semi-Detailed Lesson Plan in seconds.")

# Setup API Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("API Key not found.")
    st.stop()

# Input Guru
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("Lesson Topic:", "Ex: Photosynthesis")
    grade_level = st.selectbox("Grade Level:", ["Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Junior High (G7-10)", "Senior High (G11-12)"])
with col2:
    duration = st.slider("Class Duration (Minutes):", 30, 90, 60)
    subject = st.text_input("Subject:", "Ex: Science / Makabayan")

if st.button("Generate Lesson Plan ✨"):
    if not topic:
        st.warning("Please enter a topic first, Ma'am!")
    else:
        with st.spinner("Drafting your Lesson Plan..."):
            prompt = f"""
            Create a Semi-Detailed Lesson Plan for {grade_level} students in the Philippines.
            Subject: {subject}
            Topic: {topic}
            Duration: {duration} minutes.
            
            Strictly follow this structure (Standard DepEd Style):
            I. OBJECTIVES
               (Please include Cognitive, Psychomotor, and Affective objectives)
            II. SUBJECT MATTER
               - Topic
               - References
               - Materials
               - Values Integration
            III. PROCEDURE
               A. Preparatory Activities (Drill, Review, Unlocking of Difficulties)
               B. Motivation
               C. Lesson Proper (Activity, Analysis, Abstraction)
               D. Application
               E. Generalization
            IV. EVALUATION (5-item short quiz)
            V. ASSIGNMENT
            """
            response = model.generate_content(prompt)
            st.markdown(response.text)