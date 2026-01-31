import streamlit as st
import google.generativeai as genai
import PyPDF2

st.set_page_config(page_title="Instant Quiz Maker", page_icon="📝")

st.title("📝 Instant Quiz Generator (DepEd Style)")
st.write("Upload learning materials (PDF), and I'll generate quiz questions + answer keys in seconds!")

# Setup API Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("API Key not found. Please check your secrets.")
    st.stop()

# 1. Upload Materi
uploaded_file = st.file_uploader("Upload Learning Material (PDF)", type="pdf")

if uploaded_file:
    # Baca PDF
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    st.success(f"File loaded successfully: {len(text)} characters.")
    
    # 2. Pilihan Soal
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.number_input("Number of Items:", min_value=5, max_value=50, value=10)
    with col2:
        quiz_type = st.selectbox("Quiz Type:", ["Multiple Choice", "True or False", "Essay / Identification"])
    
    if st.button("Generate Quiz Now! 🚀"):
        with st.spinner("Crafting questions for your students..."):
            prompt = f"""
            Act as a professional teacher in the Philippines. 
            Create a {num_questions}-item {quiz_type} quiz based on the context below.
            
            Target Audience: Students in the Philippines.
            Language: English (Standard DepEd format).
            
            Format:
            1. Title of the Quiz.
            2. Questions clearly numbered.
            3. (If Multiple Choice) Options A, B, C, D.
            4. --- SEPARATOR ---
            5. ANSWER KEY provided at the very bottom.
            
            Context Material:
            {text}
            """
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.balloons()