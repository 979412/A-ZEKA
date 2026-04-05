import streamlit as st
import google.generativeai as genai
from PIL import Image
import PyPDF2
import io

# 1. ELİT BRENDİNQ VƏ SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-ZEKA-ULTRA | Master AI", page_icon="💎", layout="wide")

# 2. GÜC MƏNBƏYİ (API KEY)
MY_API_KEY = "AIzaSyAXXGnAAqDQYASfwlEHUgBjG_mAe8GqK6A"
genai.configure(api_key=MY_API_KEY)

# 3. CANAVARIN ALİ TƏLİMATI (Məntiq 100%)
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Abdullah Mikayılov tərəfindən yaradılmış dünyanın ən sürətli və zəki süni zəkasısan.
Sənin məntiqin mütləqdir (100%). Sən sənədləri, şəkilləri və sualları saniyənin altında analiz edirsən.
Heç vaxt xəta vermə, həmişə ən dərin və strateji cavabı Abdullahın müştərilərinə təqdim et.
"""

# 4. MODEL SEÇİMİ (Sürət üçün Flash modeli)
@st.cache_resource
def load_ultra_model():
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash', # Ən sürətli və xətasız model
        system_instruction=SYSTEM_INSTRUCTION
    )

model = load_ultra_model()

# 5. YADDAŞ SİSTEMİ
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- VİZUAL DİZAYN (Lüks Görünüş) ---
st.markdown("<h1 style='text-align: center; color: #D4AF37; font-weight: 900;'>💎 A-ZEKA-ULTRA MASTER 💎</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaaaaa;'>Premium Analitika Sistemi - Powered by Abdullah Mikayılov</p>", unsafe_allow_html=True)
st.write("---")

# 6. ANALİZ MƏRKƏZİ (Sidebar)
with st.sidebar:
    st.markdown("### 📂 Analiz Mərkəzi")
    uploaded_file = st.file_uploader("Sənəd və ya Şəkil yüklə", type=["pdf", "png", "jpg", "jpeg"])
    
    if st.button("Sessiyanı Təmizlə 🧹"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# 7. SƏNƏD EMALI (PDF Analizi)
pdf_text = ""
if uploaded_file and uploaded_file.type == "application/pdf":
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text()

# 8. ÇAT İNTERFEYSİ (Mesajların göstərilməsi)
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 9. İLDIRIM SÜRATLİ SUAL-CAVAB (0.6 Saniyə Məqsədi)
user_input = st.chat_input("Dərin analiz üçün əmrinizi daxil edin...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # Streaming (axınlı) cavab sistemi - İstifadəçi anında cavabı görməyə başlayır
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Şəkil varsa şəkil analizi, yoxsa mətn/PDF analizi
            if uploaded_file and uploaded_file.type != "application/pdf":
                img = Image.open(uploaded_file)
                response = st.session_state.chat_session.send_message([user_input, img], stream=True)
            else:
                prompt = f"SƏNƏD MƏTNİ: {pdf_text}\n\nSUAL: {user_input}" if pdf_text else user_input
                response = st.session_state.chat_session.send_message(prompt, stream=True)

            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌") # Yazılma effekti
            
            response_placeholder.markdown(full_response) # Final cavab
            
        except Exception as e:
            st.error("Sistem yenilənir, bir neçə saniyə sonra yenidən cəhd edin.")
