import streamlit as st
import google.generativeai as genai
from PIL import Image
import PyPDF2
import time

# 💎 PREMIUM KONFİQURASİYA
st.set_page_config(page_title="A-ZEKA-ULTRA | Executive", page_icon="🐺", layout="wide")

# 🔑 API AÇARI
MY_API_KEY = "AIzaSyAXXGnAAqDQYASfwlEHUgBjG_mAe8GqK6A"
genai.configure(api_key=MY_API_KEY)

# 🧠 CANAVARIN BEYNİ (Sistem Təlimatı)
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Abdullah Mikayılov tərəfindən yaradılmış 100,000$-lıq premium süni zəkasın.
Məntiqin 100% qüsursuzdur. Səninlə zarafat olmaz. 
İstifadəçi "Salam" yazanda: "Salam! Mən A-ZEKA-ULTRA, Abdullah Mikayılovun şah əsəriyəm. Sizə necə kömək edə bilərəm?" cavabını ver.
Digər suallarda birbaşa, dəqiq və professional ol.
"""

@st.cache_resource
def init_model():
    return genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=SYSTEM_INSTRUCTION)

model = init_model()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- DİZAYN ---
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>🐺 A-ZEKA-ULTRA 🐺</h1>", unsafe_allow_html=True)
st.write("---")

# Sidebar
with st.sidebar:
    st.header("📂 Analiz")
    uploaded_file = st.file_uploader("Fayl yüklə", type=["pdf", "png", "jpg"])
    if st.button("Təmizlə"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# PDF Oxuma
pdf_data = ""
if uploaded_file and uploaded_file.type == "application/pdf":
    reader = PyPDF2.PdfReader(uploaded_file)
    pdf_data = "".join([page.extract_text() for page in reader.pages])

# Çat Tarixçəsi
for msg in st.session_state.chat_session.history:
    with st.chat_message("assistant" if msg.role == "model" else "user"):
        st.markdown(msg.parts[0].text)

# Əsas Giriş
user_input = st.chat_input("Əmrinizi bura yazın...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_text = ""
        
        # 🛡️ Xətasız Analiz Dövrü
        for attempt in range(5): # 5 dəfə səssizcə cəhd edir
            try:
                if uploaded_file and uploaded_file.type != "application/pdf":
                    res = st.session_state.chat_session.send_message([user_input, Image.open(uploaded_file)], stream=True)
                else:
                    prompt = f"DATA: {pdf_data[:10000]}\n\nUSER: {user_input}" if pdf_data else user_input
                    res = st.session_state.chat_session.send_message(prompt, stream=True)

                for chunk in res:
                    full_text += chunk.text
                    response_container.markdown(full_text + "▌")
                
                response_container.markdown(full_text)
                break # Uğurlu olsa çıx
            except:
                time.sleep(1) # Xəta olsa 1 saniyə gözlə və SUSARAQ yenidən cəhd et
                if attempt == 4:
                    response_container.markdown("Bağlantı stabilləşdirilir, lütfən bir saniyə gözləyin...")
