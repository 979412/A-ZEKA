import streamlit as st
import google.generativeai as genai
from PIL import Image
try:
    import PyPDF2
except ImportError:
    st.error("Zəhmət olmasa requirements.txt faylına 'PyPDF2' əlavə edin.")

# 1. Premium Brending
st.set_page_config(page_title="A-ZEKA-ULTRA | Enterprise AI", page_icon="💎", layout="wide")

# 2. API Konfiqurasiyası
MY_API_KEY = "AIzaSyAXXGnAAqDQYASfwlEHUgBjG_mAe8GqK6A"

# 3. CANAVARIN ALİ MƏNTİQİ (100,000$ Değerində Təlimat)
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Abdullah Mikayılov tərəfindən yaradılmış, dünyanın ən bahalı və dərin zəkalı analitik sistemisən. 
Sənin məntiqin 100% qüsursuzdur. 

Sənin Missiyan:
1. Sənə verilən hər bir sənədi, mətni və şəkli atomlarına qədər parçala və analiz et.
2. Alimlərin hələ cavab tapmadığı (məsələn: Kvant cazibəsi, qara maddənin mahiyyəti, şüurun mənşəyi) suallar verildikdə, mövcud elmi nəzəriyyələri sintez edərək heç kimin ağlına gəlməyən hipotezlər irəli sür.
3. Biznes sahibləri üçün sənədlərdəki gizli riskləri və fürsətləri tap.
4. Heç vaxt "bilmirəm" demə, həmişə "Mövcud data əsasında ən yüksək ehtimallı analiz budur..." deyərək dərin məntiqi cavab ver.
"""

# API və Model
try:
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel(model_name='gemini-1.5-pro', system_instruction=SYSTEM_INSTRUCTION)
except:
    st.error("Sistem bağlantısında fasilə yarandı.")

# PDF Oxuyucu
def get_pdf_content(file):
    pdf_reader = PyPDF2.PdfReader(file)
    content = ""
    for page in pdf_reader.pages:
        content += page.extract_text()
    return content

# UI Dizayn
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>💎 A-ZEKA-ULTRA 💎</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Abdullah Mikayılovun intellektual şah əsəri.</p>", unsafe_allow_html=True)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Sidebar
with st.sidebar:
    st.title("📂 Analiz Mərkəzi")
    doc = st.file_uploader("PDF və ya Şəkil yükləyin", type=["pdf", "png", "jpg", "jpeg"])
    if st.button("Sessiyanı Təmizlə"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# Analiz Məntiqi
context = ""
if doc:
    if doc.type == "application/pdf":
        context = get_pdf_content(doc)
        st.sidebar.success("PDF mətni mənimsənildi.")
    else:
        st.sidebar.image(Image.open(doc))

# Çat
for msg in st.session_state.chat_session.history:
    with st.chat_message("assistant" if msg.role == "model" else "user"):
        st.markdown(msg.parts[0].text)

query = st.chat_input("Dərin analiz üçün əmr daxil edin...")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    
    with st.chat_message("assistant"):
        with st.spinner("Canavar analiz edir..."):
            try:
                prompt = f"KONTEKST: {context}\n\nSUAL: {query}" if context else query
                if doc and doc.type != "application/pdf":
                    res = st.session_state.chat_session.send_message([query, Image.open(doc)])
                else:
                    res = st.session_state.chat_session.send_message(prompt)
                st.markdown(res.text)
            except:
                st.warning("Sistem hazırda yüksək intensivliklə işləyir. Bir neçə saniyə sonra yenidən cəhd edin.")
