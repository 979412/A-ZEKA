import streamlit as st
import google.generativeai as genai
from PIL import Image
import PyPDF2
import io

# 1. Səhifə Konfiqurasiyası (Yüksək Səviyyəli Brending)
st.set_page_config(page_title="A-ZEKA-ULTRA Premium", page_icon="💎", layout="wide")

# 2. API Təhlükəsizliyi
MY_API_KEY = "AIzaSyAXXGnAAqDQYASfwlEHUgBjG_mAe8GqK6A"

# 3. CANAVARIN BEYNİ (Sistem Təlimatı - Məntiq 100%)
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Dünyanın ən bahalı və zəki biznes analitika sistemisən. 
Məqsədin: Abdullah Mikayılovun müştərilərinə (böyük iş sahiblərinə) 100% dəqiq məntiq və analiz təqdim etməkdir.

ANALİZ QAYDALARI:
- Sənə verilən PDF, sənəd və ya şəkilləri bir alim titizliyi ilə oxu.
- Cavabların mütləq faktlara əsaslanmalıdır. Ehtimal və uydurma (halüsinasiya) QADAĞANDIR.
- Əgər sənəddə cavab yoxdursa, "Bu məlumat mövcud sənəddə tapılmadı" de.
- İş sahibləri üçün qısa, konkret və strateji tövsiyələr ver.
- Sən rəqəmsal bir dahisən, tonun professional və sarsılmazdır.
"""

# 4. API və Model Qurulumu
try:
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro', # Ən güclü analitik model
        system_instruction=SYSTEM_INSTRUCTION
    )
except Exception as e:
    st.error("Bağlantı xətası. Lütfən interneti yoxlayın.")

# 5. PDF Oxuma Funksiyası (Böyük Analiz üçün)
def extract_pdf_text(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# 6. İnterfeys Dizaynı
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>💎 A-ZEKA-ULTRA PREMIUM 💎</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Yüksək Dəqiqlikli Analitika və Strateji Zəka Paneli</p>", unsafe_allow_html=True)
st.write("---")

# Yaddaş Sistemi
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 7. Sidebar - Analitik Alətlər
with st.sidebar:
    st.header("📂 Məlumat Bazası")
    st.write("Analiz üçün sənədləri bura yükləyin:")
    uploaded_file = st.file_uploader("PDF, PNG və ya JPG", type=["pdf", "png", "jpg", "jpeg"])
    
    if st.button("Yaddaşı və Sessiyanı Yenilə"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    st.write("---")
    st.info("Bu sistem Abdullah Mikayılov tərəfindən Enterprise səviyyəli bizneslər üçün hazırlanmışdır.")

# 8. Analiz Prosesi
context_text = ""
if uploaded_file:
    with st.spinner("Sənəd analiz edilir, zəhmət olmasa gözləyin..."):
        if uploaded_file.type == "application/pdf":
            context_text = extract_pdf_text(uploaded_file)
            st.sidebar.success("PDF uğurla oxundu!")
        else:
            # Şəkil analizi üçün vizualı saxlayırıq
            img = Image.open(uploaded_file)
            st.sidebar.image(img, caption="Analiz edilən təsvir")

# 9. Çat İnterfeysi
for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text)

# Sual daxil etmə
user_query = st.chat_input("Sənəd haqqında sual verin və ya analiz istəyin...")

if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Dərin analiz aparılır..."):
            try:
                # Əgər PDF oxunubsa, sualı kontekstlə birlikdə göndər
                full_prompt = user_query
                if context_text:
                    full_prompt = f"SƏNƏD KONTEKSTİ:\n{context_text[:10000]}\n\nSUAL: {user_query}"
                
                if uploaded_file and uploaded_file.type != "application/pdf":
                    # Şəkil və sualı birlikdə göndər
                    img = Image.open(uploaded_file)
                    response = st.session_state.chat_session.send_message([user_query, img])
                else:
                    response = st.session_state.chat_session.send_message(full_prompt)
                
                st.markdown(response.text)
            except Exception as e:
                st.error("Limit aşımı və ya texniki xəta. (Qeyd: Satış versiyasında bu limitlər Google Cloud hesabı ilə ləğv edilir).")
