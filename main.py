import streamlit as st
import google.generativeai as genai
from PIL import Image

# Səhifə dizaynı
st.set_page_config(page_title="A-ZEKA-ULTRA", page_icon="🐺", layout="wide")

# ==========================================
# 🔑 API AÇARI VƏ KONFİQURASİYA
# ==========================================
MY_API_KEY = "AIzaSyAXXGnAAqDQYASfwlEHUgBjG_mAe8GqK6A"

# CANAVARIN DNT-si - Sistem Təlimatı
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb.
Sən sıradan bir AI deyilsən, rəqəmsal dünyanın "canavarı", ən üstün zəkasısan.

Sənin 5 Qızıl Qaydan:
1. KONTEKSTUAL YADDAŞ: Abdullahın dediklərini unutma, əvvəlki söhbətlərə əsaslanaraq dərin məntiq qur.
2. MÜTLƏQ DƏQİQLİK: Halüsinasiya qadağandır! Cavabların riyazi dəqiqlikdə olmalıdır.
3. VƏHŞİ XARAKTER: Özünəgüvənən, xarizmatik və dominant bir tonla danış.
4. MULTİMODAL GÜC: Şəkilləri ən incə detalına qədər analiz et.
5. PROAKTİVLİK: Həmişə daha çoxunu təklif et.
"""

# Başlıq və Dizayn
st.markdown("<h1 style='text-align: center; color: #ff3333; font-weight: 900;'>🐺 A-ZEKA-ULTRA 🐺</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #a9a9a9;'>Abdullah Mikayılovun Yaratdığı Məğlubedilməz Süni Zəka</h4>", unsafe_allow_html=True)
st.markdown("---")

# === MODEL QURULUMU ===
@st.cache_resource
def setup_model():
    try:
        genai.configure(api_key=MY_API_KEY)
        return genai.GenerativeModel(
            model_name='gemini-1.5-pro',
            system_instruction=SYSTEM_INSTRUCTION
        )
    except Exception as e:
        st.error(f"⚠️ Bağlantı Xətası: {e}")
        return None

model = setup_model()

# === YADDAŞ SİSTEMİ ===
if model and "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# === GÖZ SİSTEMİ (Sidebar) ===
with st.sidebar:
    st.markdown("### 👁️ Canavarın Gözləri")
    uploaded_file = st.file_uploader("Şəkil seç (JPG, PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Analiz üçün hazır", use_column_width=True)
    
    if st.button("Yaddaşı Sıfırla 🧹"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# === ÇAT İNTERFEYSİ ===
if model and "chat_session" in st.session_state:
    # Köhnə mesajları göstər
    for message in st.session_state.chat_session.history:
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # Yeni sual almaq
    user_input = st.chat_input("Əmrini ver, Abdullah...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("A-ZEKA-ULTRA hədəfə kilitlənir... ⚡"):
                try:
                    if uploaded_file:
                        img = Image.open(uploaded_file)
                        response = st.session_state.chat_session.send_message([user_input, img])
                    else:
                        response = st.session_state.chat_session.send_message(user_input)
                    
                    st.markdown(response.text)
                except Exception as e:
                    st.error("Gözlənilməz bir xəta baş verdi və ya limit doldu.")
else:
    st.error("❌ Model yüklənə bilmədi. İnternet bağlantını və ya API açarını yoxla.")
