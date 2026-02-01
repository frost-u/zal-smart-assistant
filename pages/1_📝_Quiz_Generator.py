import streamlit as st
import google.generativeai as genai
import PyPDF2

st.set_page_config(page_title="Instant Quiz Maker", page_icon="📝")

st.title("📝 Instant Quiz Generator")
st.write("Upload multiple PDFs, select your preferred language, and get a ready-to-use quiz!")

# Setup API Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("API Key not found. Please check your secrets.")
    st.stop()

# 1. SIDEBAR SETTINGS (Supaya Rapi)
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Fitur Bahasa yang Kamu Minta
    language_option = st.selectbox(
        "Quiz Language Output:",
        ["Auto-Detect (Match Document)", "English (Standard)", "Tagalog/Filipino", "Cebuano/Bisaya", "Bahasa Indonesia"]
    )
    
    difficulty = st.select_slider(
        "Difficulty Level:",
        options=["Easy", "Medium", "Hard/HOTS"],
        value="Medium"
    )

# 2. UPLOAD FILES (Bisa Banyak File)
uploaded_files = st.file_uploader("Upload Learning Materials (PDF)", type="pdf", accept_multiple_files=True)

if uploaded_files:
    text = ""
    # Loop untuk baca semua file
    for pdf_file in uploaded_files:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
            
    # Feedback UI dalam Bahasa Inggris
    st.success(f"✅ Successfully loaded {len(uploaded_files)} file(s). Total content: {len(text)} characters.")
    
    # 3. QUIZ SETTINGS
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.number_input("Number of Items:", min_value=5, max_value=50, value=10)
    with col2:
        quiz_type = st.selectbox("Quiz Type:", ["Multiple Choice", "True or False", "Essay / Identification"])
    
    if st.button("Generate Quiz Now! 🚀"):
        with st.spinner("Analyzing documents & crafting questions..."):
            
            # Logic Prompt Adaptif
            lang_instruction = ""
            if language_option == "Auto-Detect (Match Document)":
                lang_instruction = "Detect the language of the provided text and write the quiz IN THAT SAME LANGUAGE."
            else:
                lang_instruction = f"Write the quiz strictly in {language_option} language."

            prompt = f"""
            Act as a professional teacher.
            Create a {num_questions}-item {quiz_type} quiz based on the context below.
            
            Configuration:
            - Difficulty: {difficulty}
            - Language: {lang_instruction}
            
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

elif not uploaded_files:
    st.info("👋 Please upload your PDF materials above to start.")