import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Smart Audio", page_icon="🎙️")

st.title("🎙️ Smart Audio")
st.write("Upload voice notes, meetings, or interviews. AI will listen and summarize them for you.")

# Setup API Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # --- UPDATE: MENGGUNAKAN GEMINI 2.5 FLASH ---
    # Model ini dipilih karena tersedia di akunmu dan sangat cepat untuk audio
    model = genai.GenerativeModel('gemini-2.5-flash')
    # --------------------------------------------
    
except Exception as e:
    st.error("API Key not found. Please check your secrets.")
    st.stop()

# 1. Upload Audio
audio_file = st.file_uploader("Upload Audio File...", type=["mp3", "wav", "m4a", "ogg"])

if audio_file is not None:
    # Display audio player
    st.audio(audio_file)
    
    # 2. User Instruction
    prompt = st.text_input("Instruction for AI:", 
                           value="Transcribe this audio and summarize the key points.")

    if st.button("Analyze Audio 🎧"):
        with st.spinner("Listening to the audio..."):
            try:
                # Read audio data
                audio_bytes = audio_file.read()
                
                # Send to Gemini (Audio + Text Prompt)
                response = model.generate_content([
                    prompt,
                    {
                        "mime_type": audio_file.type,
                        "data": audio_bytes
                    }
                ])
                
                st.success("Analysis Result:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Failed to process audio. Error: {e}")