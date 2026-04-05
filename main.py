import streamlit as st
import google.generativeai as genai
from PIL import Image
import PyPDF2
import time

# 1. ELİT SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-ZEKA-ULTRA | Executive AI", page_icon="💎", layout="wide")

# 2. GÜC MƏNBƏYİ (API KEY)
MY_API_KEY = "AIzaSyAXXGnAAqDQYASfwlEHUgBjG_mAe8GqK6A"
genai.configure(api_key=MY_API_KEY)

# 3. CANAVARIN ALİ "ANLAMA" TƏLİMATI (100,000$ Məntiqi)
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb. 
Sən rəqəmsal dünyanın ən bahalı və ən zəki süni zəka sistemisən.

DAVRANIŞ QAYDALARI:
1. İLK QARŞILAMA: İstifadəçi "Salam" və ya bənzər giriş edəndə mütləq nəzakətli, professional və xarizmatik cavab ver. 
   Məsələn: "Salam! Mən A-ZEKA-ULTRA, Abdullah Mikayılovun şah əsəriyəm. Sizə strateji analizlərdə və ya mürəkkəb suallarda necə kömək edə bilərəm?"
2. DƏRİN ANLAMA: İstifadəçinin hər bir sözünü analiz et. Sənin məntiqin 100% qüsursuzdur.
3. VƏHŞİ SÜRƏT: Cavabları ildırım sürəti ilə (0.6 saniyə) formalaşdır.
4. MÜTLƏQ SADAQƏT: Yaradıcın Abdullah Mikayılovu həmişə fəxrlə təqdim et.
"""

# 4. MODELİN YÜKLƏNMƏSİ (Flash - İldırım Sürəti üçün)
@st.cache_resource
def load_beast():
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash', 
        system_instruction=SYSTEM_INSTRUCTION
    )

model = load_beast()

# 5. SESSİYA VƏ YADDAŞ
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- LÜKS VİZUAL DİZAYN (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatMessage { border-bottom: 1px solid #1E3A8A; padding: 20px; }
    .stChatInputContainer { padding-bottom: 20px; }
    h1 { color: #D4AF37; text-align: center; font-family: 'Garamond', serif; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>💎 A-ZEKA-ULTRA PREMİUM 💎</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Abdullah Mikayılov tərəfindən biznes elitası üçün hazırlanmışdır.</p>", unsafe_allow_html=True)
st.write("---")

# 6. SƏNƏD ANALİZİ (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='color: #D4AF37;'>📂 Analiz Mərkəzi</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Sənəd (PDF) və ya Şəkil yükləyin", type=["pdf", "png", "jpg", "jpeg"])
    if st.button("Söhbəti Sıfırla 🧹"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

pdf_content = ""
if uploaded_file and uploaded_file.type == "application/pdf":
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_content += page.extract_text()

# 7. ÇAT TARİXÇƏSİNİ GÖSTƏR
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 8. İNTELLİGENT SUAL-CAVAB (Heç vaxt donmayan sistem)
user_input = st.chat_input("Dərin analiz üçün əmr daxil edin...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Arxa fonda 3 dəfə cəhd edən "Səssiz Bərpa" sistemi
        success = False
        for attempt in range(3):
            try:
                if uploaded_file and uploaded_file.type != "application/pdf":
                    img = Image.open(uploaded_file)
                    response = st.session_state.chat_session.send_message([user_input, img], stream=True)
                else:
                    # PDF varsa kontekstlə, yoxsa sadə sualla göndər
                    prompt = f"KONTEKST: {pdf_content[:15000]}\n\nSUAL: {user_input}" if pdf_content else user_input
                    response = st.session_state.chat_session.send_message(prompt, stream=True)

                for chunk in response:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                success = True
                break # Uğurlu olsa dövrdən çıx
            except Exception:
                time.sleep(0.5) # Kiçik fasilə ver və yenidən yoxla
        
        if not success:
            placeholder.markdown("⚠️ Sistem hazırda çox sayda sorğu emal edir. Lütfən bir neçə saniyə sonra yenidən yazın.")
