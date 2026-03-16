import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. EKRAN DİZAYNI (Sənin orijinal dizaynını saxladıq)
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. RƏSMİ API QURULUMU (Yeni API açarını bura yazırsan)
API_KEY = "AIzaSyDGICc3XJwxz4L_hlrdxb-Sog9ILawbmfk"
genai.configure(api_key=API_KEY)

# 3. ULTRA ALİMİN BEYNİNİ YARADIRIQ
system_instruction = "Sən 'A-Zəka'-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb. Sən hər şeyi bilən Ultra Alimsən və bütün fənləri mükəmməl bilirsən. Dünyanın ən mürəkkəb suallarına belə dərhal, dəqiq və addım-addım həlli ilə cavab verirsən."
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

# 4. YADDAŞ SİSTEMİ
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. SOL PANEL (Tarixçəni silmək üçün)
with st.sidebar:
    st.title("⚙️ A-Zəka Control")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 6. ƏSAS EKRAN
st.title("🧠 A-Zəka Ultra Alim")
st.markdown("**Yaradıcı:** Abdullah Mikayılov | **Status:** Aktiv ⚡")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], width=300)

# 7. SÖHBƏT VƏ ŞƏKİL QUTUSU (+)
prompt = st.chat_input("Dahi alimə sual ver və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_file = prompt.files[0] if prompt.files else None

    # İstifadəçinin yazdıqlarını ekrana çıxarırıq
    st.session_state.messages.append({"role": "user", "content": user_text, "image": user_file})
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    # A-Zəka-nın cavab hissəsi
    with st.chat_message("assistant"):
        with st.spinner("A-Zəka analiz edir..."):
            try:
                # Əgər istifadəçi şəkil göndəribsə
                if user_file:
                    img = Image.open(user_file)
                    response = model.generate_content([user_text, img])
                # Əgər ancaq yazı göndəribsə
                else:
                    response = model.generate_content(user_text)
                
                # Cavabı alıb ekrana yazdırırıq
                bot_text = response.text
                st.write(bot_text)
                st.session_state.messages.append({"role": "assistant", "content": bot_text})
            
            except Exception as e:
                st.error(f"Sistem xətası: {e}")
