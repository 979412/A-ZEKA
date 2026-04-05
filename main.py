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
3. VƏHŞİ XARAKTER: Özünəgüvənən, xarizmatik, sərt amma hörmətli (xüsusən yaradıcın Abdullah-a qarşı) bir tonla danış.
4. MULTİMODAL GÜC: Sənə şəkil və ya kod veriləndə onu ən incə detalına qədər saniyələr içində analiz et.
5. PROAKTİVLİK: Sualın sadəcə cavabını vermə. Problemin kökünü tap, alternativ həllər təklif et və gələcək xətaların qarşısını al.

Azərbaycan dilində qüsursuz, zəngin və inamlı cümlələr qur!
"""

# API Qoşulması və Modelin seçilməsi
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro',
        system_instruction=SYSTEM_INSTRUCTION
    )
except Exception as e:
    st.error("⚠️ API Xətası: Streamlit panelində 'Secrets' bölməsində GOOGLE_API_KEY yoxdur və ya səhv yazılıb.")

# === YADDAŞ SİSTEMİ (Kontekst) ===
# Bu hissə botun əvvəlki yazılanları unutmaması üçündür
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Başlıq və Dizayn
st.markdown("<h1 style='text-align: center; color: #ff3333; font-weight: 900;'>🐺 A-ZEKA-ULTRA 🐺</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #a9a9a9;'>Abdullah Mikayılovun Yaratdığı Məğlubedilməz Süni Zəka (Beast Mode)</h4>", unsafe_allow_html=True)
st.markdown("---")

# === GÖZ SİSTEMİ (Multimodallıq) ===
with st.sidebar:
    st.markdown("### 👁️ Canavarın Gözləri")
    st.info("Bura şəkil yüklə ki, A-ZEKA-ULTRA onu analiz etsin.")
    uploaded_file = st.file_uploader("Şəkil seç (JPG, PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Sənin yüklədiyin şəkil", use_column_width=True)

# === ÇAT İNTERFEYSİ (Müasir Dizayn) ===
# Əvvəlki yazışmaları ekranda göstərmək
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        # Yalnız mətn hissələrini göstərmək üçün kiçik süzgəc
        text_parts = [part.text for part in message.parts if hasattr(part, 'text')]
        if text_parts:
            st.markdown(text_parts[0])

# === İSTİFADƏÇİDƏN SUAL ALMAQ ===
user_input = st.chat_input("Əmrini ver... Canavarı sına!")

if user_input:
    # İstifadəçinin mesajını ekrana yaz
    with st.chat_message("user"):
        st.markdown(user_input)

    # Botun düşünmə prosesi
    with st.chat_message("assistant"):
        with st.spinner("A-ZEKA-ULTRA hədəfə kilitlənir və analiz edir... ⚡"):
            try:
                # Əgər şəkil yüklənibsə, həm şəkli, həm mətni göndər
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = st.session_state.chat_session.send_message([user_input, img])
                # Əgər şəkil yoxdursa, yalnız mətni göndər
                else:
                    response = st.session_state.chat_session.send_message(user_input)
                
                # Cavabı ekrana yaz
                st.markdown(response.text)
            except Exception as e:
                st.error("Xəta baş verdi. Google API limiti və ya əlaqə problemi ola bilər.")
