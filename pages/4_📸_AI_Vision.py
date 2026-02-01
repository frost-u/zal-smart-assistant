import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Vision", page_icon="📸")

st.title("📸 AI Vision")
st.write("Upload any image (Wedding venue, Receipt, Sketches), and AI will analyze it.")

# Setup API Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("API Key not found.")
    st.stop()

# 1. Upload Image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    # 2. User Question
    st.write("---")
    user_prompt = st.text_input("What do you want to know about this image?", 
                                placeholder="Ex: Estimate the cost of this decoration, or describe the style.")

    if st.button("Analyze Image 🔍"):
        if not user_prompt:
            st.warning("Please ask a question first.")
        else:
            with st.spinner("Analyzing image details..."):
                try:
                    # --- MAGIC HAPPENS HERE ---
                    response = model.generate_content([user_prompt, image])
                    
                    st.success("Analysis Result:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")