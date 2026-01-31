import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Wedding Consultant", page_icon="💍")

st.title("💍 AI Wedding & Finance Assistant (Level 2)")
st.write("Upload brosur gedung, daftar katering, atau catatan keuanganmu. AI akan menganalisanya!")

# --- 2. SETUP AI ---
# Ambil API Key dari Secrets (Aman)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("API Key belum disetting di .streamlit/secrets.toml atau di Cloud!")
    st.stop()

# --- 3. SIDEBAR (Fitur Upload) ---
with st.sidebar:
    st.header("📂 Data Pendukung")
    uploaded_file = st.file_uploader("Upload PDF (Brosur/Catatan)", type="pdf")
    
    pdf_text = ""
    # Jika ada file diupload, baca isinya
    if uploaded_file is not None:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                pdf_text += page.extract_text()
            st.success(f"Berhasil membaca {len(reader.pages)} halaman!")
        except Exception as e:
            st.error("Gagal membaca file PDF.")

# --- 4. USER INTERFACE ---
# Tampilkan info jika ada data PDF yang masuk
if pdf_text:
    st.info("✅ AI sekarang memiliki konteks dari dokumen PDF kamu.")
else:
    st.warning("⚠️ Belum ada dokumen. AI hanya menjawab berdasarkan pengetahuan umum.")

user_input = st.text_area("Tanya sesuatu tentang pernikahan/dokumenmu:", height=100)

if st.button("Analisa & Jawab 🤖"):
    if not user_input:
        st.warning("Tulis pertanyaan dulu ya!")
    else:
        with st.spinner('Sedang berpikir keras...'):
            try:
                # --- TEKNIK RAG SIMPLE ---
                # Kita menggabungkan Isi PDF + Pertanyaan User menjadi satu prompt panjang
                
                prompt_rahasia = f"""
                Kamu adalah asisten profesional.
                
                Tugasmu: Jawab pertanyaan user BERDASARKAN data yang ada di "Context" di bawah ini. 
                Jika jawabannya tidak ada di Context, gunakan pengetahuan umummu tapi beri tahu user.
                
                Context (Data dari PDF):
                {pdf_text}
                
                Pertanyaan User:
                {user_input}
                
                Jawablah dengan ramah dan terstruktur (gunakan poin-poin).
                """
                
                response = model.generate_content(prompt_rahasia)
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.divider()
st.caption("AI Smart Reader by Faizal")

# Update paksa