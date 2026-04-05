import streamlit as st
import google.generativeai as genai
from PIL import Image
import PyPDF2
import time

# 1. ELİT BRENDİNQ
st.set_page_config(page_title="A-ZEKA-ULTRA PRO", page_icon="💎", layout="wide")

# 2. GÜC MƏNBƏYİ (API KEY)
MY_API_KEY = "AIzaSyAXXGnAAqDQYASfwlEHUgBjG_mAe8GqK6A"
genai.configure(api_key=MY_API_KEY)

# 3. CANAVARIN ALİ TƏLİMATI
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Abdullah Mikayılov tərəfindən yaradılmış dünyanın ən sürətli süni zəkasısan.
Sənin məntiqin 100% dəqiqdir. Cavabların qısa, kəskin və strateji olmalıdır. 
İş adamları üçün saniyələr vacibdir, ona görə də vaxt itirmədən birbaşa hədəfə vuran cavablar ver.
"""

# 4. MODELİ YÜKLƏ (Yüksək Sürətli Flash Modeli)
@st.cache_resource
def load_beast_model():
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash', 
        system_instruction=SYSTEM_INSTRUCTION
    )

model = load_beast_model()

# 5. YADDAŞ VƏ SESSİYA
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- DİZAYN (CSS ilə Gözəlləşdirmə) ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInput { border: 2px solid #D4AF37 !important; }
    h1 { text-shadow: 2px 2px #000; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #D4AF37;'>💎 A-ZEKA-ULTRA MASTER 💎</h1>", unsafe_allow_html=True)
st.write("---")

# 6. SƏNƏD ANALİZİ (Sidebar)
with st.sidebar:
    st.markdown("### 👁️ Analiz Mərkəzi")
    uploaded_file = st.file_uploader("PDF və ya Şəkil", type=["pdf", "png", "jpg", "jpeg"])
    if st.button("Söhbəti Sıfırla 🧹"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

pdf_text = ""
if uploaded_file and uploaded_file.type == "application/pdf":
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text()

# 7. MESAJ TARİXÇƏSİ
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 8. "HEÇ VAXT XƏTA VERMƏYƏN" SUAL-CAVAB
user_input = st.chat_input("Əmrini gözləyirəm, Abdullah...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        # Sürət və Stabillik üçün optimizasiya edilmiş dövr
        retries = 3
        while retries > 0:
            try:
                if uploaded_file and uploaded_file.type != "application/pdf":
                    img = Image.open(uploaded_file)
                    response = st.session_state.chat_session.send_message([user_input, img], stream=True)
                else:
                    prompt = f"CONTEXT: {pdf_text[:15000]}\n\nQUESTION: {user_input}" if pdf_text else user_input
                    response = st.session_state.chat_session.send_message(prompt, stream=True)

                for chunk in response:
                    full_res += chunk.text
                    placeholder.markdown(full_res + "▌")
                
                placeholder.markdown(full_res)
                break # Uğurlu olsa dövrü dayandır
                
            except Exception:
                retries -= 1
                if retries == 0:
                    placeholder.markdown("⚠️ Sistemdə qısamüddətli yüklənmə var. Lütfən təkrar daxil edin.")
                time.sleep(1) # 1 saniyə gözlə və yenidən cəhd et
