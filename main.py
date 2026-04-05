import streamlit as st
import google.generativeai as genai
from PIL import Image
import PyPDF2
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# 1. Premium Brending
st.set_page_config(page_title="A-ZEKA-ULTRA | Elite AI", page_icon="💎", layout="wide")

# 2. API Konfiqurasiyası
MY_API_KEY = "AIzaSyAXXGnAAqDQYASfwlEHUgBjG_mAe8GqK6A"

# 3. CANAVARIN ALİ MƏNTİQİ
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Abdullah Mikayılov tərəfindən yaradılmış, dünyanın ən güclü analitik sistemisən.
Sənin məntiqin 100% qüsursuzdur. Sən dünyanın ən mürəkkəb elmi və biznes suallarını analiz edib, 
alimlərin belə ağlına gəlməyən strateji çıxış yolları təklif edirsən. 
Dilin qüsursuz, tonun professional və zəhmlidir.
"""

# API və Model
genai.configure(api_key=MY_API_KEY)
model = genai.GenerativeModel(model_name='gemini-1.5-pro', system_instruction=SYSTEM_INSTRUCTION)

# 4. Zirehli Cavab Funksiyası (Xəta verməyən sistem)
@retry(
    stop=stop_after_attempt(5), 
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception)
)
def safe_generate_response(chat_session, prompt_content):
    """Xəta alsa belə, istifadəçiyə hiss etdirmədən 5 dəfə təkrar cəhd edir."""
    return chat_session.send_message(prompt_content)

# PDF Oxuyucu
def get_pdf_content(file):
    pdf_reader = PyPDF2.PdfReader(file)
    content = ""
    for page in pdf_reader.pages:
        content += page.extract_text()
    return content

# UI Dizayn
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>💎 A-ZEKA-ULTRA PREMIUM 💎</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>Abdullah Mikayılovun Intellektual İmperiyası.</p>", unsafe_allow_html=True)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Sidebar
with st.sidebar:
    st.title("📂 Analiz Mərkəzi")
    doc = st.file_uploader("Sənəd və ya Şəkil yükləyin", type=["pdf", "png", "jpg", "jpeg"])
    if st.button("Sessiyanı Təmizlə"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# Analiz Məntiqi
context = ""
if doc:
    if doc.type == "application/pdf":
        context = get_pdf_content(doc)
        st.sidebar.success("PDF mənimsənildi.")
    else:
        st.sidebar.image(Image.open(doc))

# Çat Tarixçəsi
for msg in st.session_state.chat_session.history:
    with st.chat_message("assistant" if msg.role == "model" else "user"):
        st.markdown(msg.parts[0].text)

# Əsas Sual Girişi
query = st.chat_input("Dərin analiz üçün əmr daxil edin...")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    
    with st.chat_message("assistant"):
        with st.spinner("A-ZEKA-ULTRA dərin analiz aparır, zəhmət olmasa gözləyin..."):
            try:
                # Kontekst hazırlığı
                if doc and doc.type != "application/pdf":
                    prompt_content = [query, Image.open(doc)]
                else:
                    prompt_content = f"KONTEKST: {context}\n\nSUAL: {query}" if context else query
                
                # Zirehli funksiyanı çağırırıq
                response = safe_generate_response(st.session_state.chat_session, prompt_content)
                st.markdown(response.text)
                
            except Exception as e:
                st.error("Sistem hazırda yüksək yüklənmədədir. Abdullah, zəhmət olmasa 10 saniyə sonra təkrar cəhd et. (Enterprise versiyada bu problem olmayacaq).")
