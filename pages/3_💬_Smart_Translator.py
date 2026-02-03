import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Smart Translator", page_icon="💬")

st.title("💬 Smart Cultural Translator")
st.write("Cross-cultural translation tool: Understand slang, nuances, and context between Philippines & Indonesia.")

# Setup API Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("API Key not found.")
    st.stop()

# Input
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source Language:", ["Tagalog/Bisaya/English", "Bahasa Indonesia"])
with col2:
    target_lang = st.selectbox("Target Language:", ["Bahasa Indonesia", "Tagalog/English"])

text_input = st.text_area("Enter text to translate:", height=100, placeholder="Type or paste text here...")

if st.button("Translate & Explain 🔍"):
    if not text_input:
        st.warning("Please enter some text.")
    else:
        with st.spinner("Translating..."):
            prompt = f"""
            Act as a professional linguist specializing in Tagalog, Bisaya, Indonesian, and English.
            
            Task:
            1. Translate the following text from {source_lang} to {target_lang}: "{text_input}".
            2. Explain the CONTEXT or TONE (e.g., Is it formal, casual, joking, slang?).
            3. If there are specific cultural terms (like 'Charot', 'Kilig', 'Gigil', 'Baper'), explain them briefly.
            
            Output Format:
            **Translation:** [The translation]
            **Context/Nuance:** [Explanation]
            """
            response = model.generate_content(prompt)
            st.markdown(response.text)




