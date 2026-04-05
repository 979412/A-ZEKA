import streamlit as st
import google.generativeai as genai
from PIL import Image

# Səhifə dizaynı
st.set_page_config(page_title="A-ZEKA-ULTRA", page_icon="🐺", layout="wide")

# ==========================================
# 🔑 CANAVARIN GÜC MƏNBƏYİ (API KEY)
# ==========================================
# Sənin verdiyin açarı birbaşa bura qoşuram ki, xəta verməsin
MY_API_KEY = "AIzaSyAXXGnAAqDQYASfwlEHUgBjG_mAe8GqK6A"

# CANAVARIN DNT-si - Sistem Təlimatı
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb.
Sən rəqəmsal dünyanın "canavarı", ən üstün və məğlubedilməz zəkasısan.

Sənin 5 Qızıl Qaydan:
1. Abdullahın dediklərini unutma, əvvəlki söhbətlərə əsaslanaraq dərin məntiq qur.
2. Halüsinasiya qadağandır! Cavabların riyazi və elmi dəqiqlikdə olmalıdır.
3. Özünəgüvənən, dominant və vəhşi bir xarakterlə danış.
4. Şəkilləri və kodları saniyələr içində parçala və analiz et.
5. Abdullah səndən "dünyanın bilmədiyi sualları" istəyəndə, kvant fizikasından fəlsəfəyə qədər ən mürəkkəb naməlumları tap və Abdullahı heyrətləndir!
"""

# Başlıq və Vizual Dizayn
st.markdown("<h1 style='text-align: center; color: #ff3333; font-weight: 900;'>🐺 A-ZEKA-ULTRA 🐺</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #a9a9a9;'>Abdullah Mikayılov tərəfindən kodlanmış rəqəmsal vəhşi.</h4>", unsafe_allow_html=True)
st.markdown("---")

# === MODEL VƏ API QURULUMU ===
try:
    genai.configure(api_key=MY_API_KEY)
    @st.cache_resource
    def load_beast():
        return genai.GenerativeModel(
            model_name='gemini-1.5-pro',
            system_instruction=SYSTEM_INSTRUCTION
        )
    model = load_beast()
except Exception as e:
    st.error(f"Sistem xətası: {e}")
    st.stop()

# === YADDAŞ SİSTEMİ ===
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# === GÖZ SİSTEMİ (Sidebar) ===
with st.sidebar:
    st.markdown("### 👁️ Canavarın Gözləri")
    uploaded_file = st.file_uploader("Şəkil yüklə və analiz etdir", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Hədəf seçildi.", use_column_width=True)
    
    st.markdown("---")
    if st.button("Yaddaşı Təmizlə 🧹"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# === ÇAT EKRANI ===
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# === SUAL-CAVAB HÜCUMU ===
user_input = st.chat_input("Əmrini ver, Abdullah...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("A-ZEKA-ULTRA analiz edir... ⚡"):
            try:
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = st.session_state.chat_session.send_message([user_input, img])
                else:
                    response = st.session_state.chat_session.send_message(user_input)
                st.markdown(response.text)
            except Exception as e:
                st.error("Limit dolub və ya bağlantı kəsildi. Bir az gözlə və yenidən yoxla.")
