import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Səhifə konfiqurasiyası
st.set_page_config(page_title="A-ZEKA-ULTRA Business", page_icon="💼", layout="wide")

# API KEY (Sənin verdiyin açar)
MY_API_KEY = "AIzaSyAXXGnAAqDQYASfwlEHUgBjG_mAe8GqK6A"

# ŞİRKƏT REJİMİ - Sistem Təlimatı
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Abdullah Mikayılov tərəfindən biznes analitika və yüksək performans üçün yaradılıbsan.
Vəzifən: Şirkət rəhbərlərinə qərar qəbulunda kömək etmək, sənədləri analiz etmək və strateji planlar qurmaqdır.
Tonun: Professional, dəqiq, ciddi və məlumatlı. 
"""

# API və Model Qurulumu
try:
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel(model_name='gemini-1.5-pro', system_instruction=SYSTEM_INSTRUCTION)
except Exception as e:
    st.error("Bağlantı xətası.")

# Yaddaş
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- DİZAYN ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🚀 A-ZEKA-ULTRA (Business Intelligence)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Böyük bizneslər üçün strateji süni zəka həlli.</p>", unsafe_allow_html=True)

# Sidebar - Sənəd və Şəkil Analizi
with st.sidebar:
    st.header("📊 Analiz Paneli")
    uploaded_file = st.file_uploader("Sənəd və ya Şəkil yüklə (PDF, PNG, JPG)", type=["pdf", "png", "jpg", "jpeg", "txt"])
    
    if st.button("Söhbəti Sıfırla"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# Çat Keçmişi
for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text)

# Əsas Giriş
user_input = st.chat_input("Biznes strategiyanız haqqında soruşun...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analiz edilir..."):
            try:
                content = [user_input]
                if uploaded_file:
                    if uploaded_file.type == "application/pdf":
                        # Sadə PDF analizi üçün bura gələcəkdə PyPDF2 əlavə edə bilərik
                        content.append("İstifadəçi sənəd yüklədi. Onu analiz et.")
                    else:
                        img = Image.open(uploaded_file)
                        content.append(img)
                
                response = st.session_state.chat_session.send_message(content)
                st.markdown(response.text)
            except Exception as e:
                st.error("Limit doldu. Biznes versiyaya keçid tövsiyə olunur.")
