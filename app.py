import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION (English) ---
st.set_page_config(page_title="Our Wedding Planner", page_icon="💍")

st.title("💍 AI Wedding & Love Assistant")
st.write("Hello! I am your personal AI assistant. Share your wedding dreams, financial worries, or LDR thoughts here.")

# --- 2. SETUP AI ---

# Ambil kunci dari brankas rahasia (secrets)
api_key = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 3. USER INTERFACE (English) ---
# Kotak input
user_input = st.text_area("What's on your mind today?", height=150, placeholder="Example: We want to get married in 2027. How should we save money starting now?")

# Tombol kirim
if st.button("Ask AI for Advice 💌"):
    if not user_input:
        st.warning("Please type something first, my friend! 😉")
    else:
        # Loading spinner in English
        with st.spinner('Thinking about the best advice for you...'):
            try:
                # --- RAHASIA DAPUR (PROMPT) ---
                # Di sini kita menyuruh AI bertingkah seperti konsultan profesional
                # Dan WAJIB menjawab dalam bahasa Inggris.
                
                prompt_khusus = f"""
                You are a wise, friendly, and supportive wedding consultant and financial advisor.
                
                Context:
                - The user is in a long-distance relationship (Philippines & Indonesia).
                - They plan to get married around 2027.
                - Please answer ONLY in English.
                - Be encouraging and give practical, easy-to-understand advice.
                
                User's Question: {user_input}
                """
                
                response = model.generate_content(prompt_khusus)
                
                # Tampilkan hasil
                st.success("Here is the advice for you:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Oops, something went wrong: {e}")

# Footer
st.divider()
st.caption("Made with ❤️ by Faizal for our future.")