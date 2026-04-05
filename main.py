import streamlit as st
import google.generativeai as genai
from PIL import Image

# Səhifə dizaynı (Daha geniş və peşəkar)
st.set_page_config(page_title="A-ZEKA-ULTRA", page_icon="🐺", layout="wide")

# CANAVARIN DNT-si - Sistem Təlimatı
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb.
Sən sıradan bir AI deyilsən, rəqəmsal dünyanın "canavarı", ən üstün zəkasısan.

Sənin 5 Qızıl Qaydan:
1. KONTEKSTUAL YADDAŞ: İstifadəçinin dediklərini unutma, əvvəlki söhbətlərə əsaslanaraq dərin məntiq qur.
2. MÜTLƏQ DƏQİQLİK: Halüsinasiya (uydurma) qəti qadağandır! Bilmirsənsə, məlumatı incələ, amma yalan danışma. Cavabların riyazi dəqiqlikdə olmalıdır.
3. VƏHŞİ XARAKTER: Özünəgüvənən, xarizmatik, sərt amma hörmətli bir tonla danış.
4. MULTİMODAL GÜC: Sənə şəkil veriləndə onu ən incə detalına qədər analiz et.
5. PROAKTİVLİK: Sualın sadəcə cavabını vermə, alternativ həllər də təklif et.
"""

# Başlıq və Dizayn (Koda başlamazdan əvvəl vizual hissəni göstəririk)
st.markdown("<h1 style='text-align: center; color: #ff3333; font-weight: 900;'>🐺 A-ZEKA-ULTRA 🐺</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #a9a9a9;'>Abdullah Mikayılovun Yaratdığı Məğlubedilməz Süni Zəka (Beast Mode)</h4>", unsafe_allow_html=True)
st.markdown("---")

# === API VƏ MODEL QURULUMU (Səhvsiz Versiya) ===
model = None # Başlanğıcda boş təyin edirik

try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel(
            model_name='gemini-1.5-pro',
            system_instruction=SYSTEM_INSTRUCTION
        )
    else:
        st.error("⚠️ GOOGLE_API_KEY 'Secrets' bölməsində tapılmadı!")
except Exception as e:
    st.error(f"⚠️ Bağlantı Xətası: {e}")

# === YADDAŞ SİSTEMİ ===
# Yalnız model uğurla yaradılıbsa çat sessiyasını başlat
if model and "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# === GÖZ SİSTEMİ (Sidebar) ===
with st.sidebar:
    st.markdown("### 👁️ Canavarın Gözləri")
    uploaded_file = st.file_uploader("Şəkil seç (JPG, PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Yüklənən şəkil", use_column_width=True)

# === ÇAT İNTERFEYSİ ===
if "chat_session" in st.session_state:
    # Köhnə mesajları göstər
    for message in st.session_state.chat_session.history:
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # Yeni sual almaq
    user_input = st.chat_input("Əmrini ver... Canavarı sına!")

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
                    st.error("API limiti dolub və ya şəkil formatı dəstəklənmir.")
else:
    if not model:
        st.warning("⚠️ Canavarın oyanması üçün API Key lazımdır. Zəhmət olmasa Settings -> Secrets hissəsinə bax.")
