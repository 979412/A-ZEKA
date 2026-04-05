import streamlit as st
import google.generativeai as genai
from PIL import Image
import PyPDF2
import time

# 💎 Brendinq
st.set_page_config(page_title="A-ZEKA-ULTRA | Elite Speed", page_icon="⚡", layout="wide")

# 🔑 API
MY_API_KEY = "AIzaSyAXXGnAAqDQYASfwlEHUgBjG_mAe8GqK6A"
genai.configure(api_key=MY_API_KEY)

# 🧠 Model Seçimi: Sürət üçün "flash" istifadə edirik
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash', # İldırım sürəti!
    system_instruction="Sən Abdullah Mikayılov tərəfindən yaradılmış A-ZEKA-ULTRA-san. Cavabların qısa, konkret və 100% dəqiq olmalıdır."
)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- UI ---
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>⚡ A-ZEKA-ULTRA SPEED ⚡</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("📊 Analiz Mərkəzi")
    doc = st.file_uploader("Sənəd yüklə", type=["pdf", "png", "jpg"])
    if st.button("Sessiyanı Təmizlə"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# Analiz Məntiqi
context = ""
if doc and doc.type == "application/pdf":
    pdf_reader = PyPDF2.PdfReader(doc)
    for page in pdf_reader.pages:
        context += page.extract_text()

# Sual daxil etmə
query = st.chat_input("Əmrini ver...")

if query:
    # Köhnə mesajları göstər
    for msg in st.session_state.chat_session.history:
        with st.chat_message("assistant" if msg.role == "model" else "user"):
            st.markdown(msg.parts[0].text)

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        response_placeholder = st.empty() # Canlı yazılma üçün yer
        full_response = ""
        
        try:
            # Sürətli cavab üçün stream=True istifadə edirik
            if doc and doc.type != "application/pdf":
                response = st.session_state.chat_session.send_message([query, Image.open(doc)], stream=True)
            else:
                prompt = f"Sənəd: {context}\nSual: {query}" if context else query
                response = st.session_state.chat_session.send_message(prompt, stream=True)

            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌") # Yazılma effekti
            
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error("Bağlantı yenilənir... Zəhmət olmasa bir daha yaz.")
