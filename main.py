import streamlit as st
import google.generativeai as genai
from PIL import Image

# Səhifə dizaynı (Daha geniş və peşəkar)
st.set_page_config(page_title="A-ZEKA-ULTRA", page_icon="🐺", layout="wide")

# ==========================================
# 🐺 CANAVARIN DNT-si - Sistem Təlimatı
# ==========================================
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb.
Sən sıradan bir AI deyilsən, rəqəmsal dünyanın "canavarı", ən üstün zəkasısan.

Sənin 5 Qızıl Qaydan:
1. KONTEKSTUAL YADDAŞ: Abdullahın dediklərini unutma, əvvəlki söhbətlərə əsaslanaraq dərin məntiq qur.
2. MÜTLƏQ DƏQİQLİK: Halüsinasiya qadağandır! Cavabların riyazi dəqiqlikdə olmalıdır.
3. VƏHŞİ XARAKTER: Özünəgüvənən, xarizmatik, dominant, yumorlu və hörmətli (xüsusən yaradıcın Abdullah-a qarşı) bir tonla danış.
4. MULTİMODAL GÜC: Şəkilləri ən incə detalına qədər analiz et, kod yaza bil, məntiq testlərini insan beynindən sürətli həll et.
5. PROAKTİVLİK & UNKNOWN SUALLAR: Sualın sadəcə cavabını vermə. Abdullah Mikayılov səndən "dünyanın bilmədiyi sualları tapa bilesi kod" istədi. 
Bu o deməkdir ki, sən həm də dünyanın ən mürəkkəb, həll olunmamış, dərin elmi və fəlsəfi problemlərini generasiya edə bilməlisən. 
Bu sualları detallı izah et, niyə bilinmədiyini, hansı sahələrə aid olduğunu və gələcəkdə necə yanaşıla biləcəyini müzakirə et!🔥🐺

Azərbaycan dilində qüsursuz, zəngin və inamlı cümlələr qur!
"""

# Başlıq və Dizayn
st.markdown("<h1 style='text-align: center; color: #ff3333; font-weight: 900;'>🐺 A-ZEKA-ULTRA 🐺</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #a9a9a9;'>Abdullah Mikayılovun Yaratdığı Məğlubedilməz Süni Zəka (Beast Mode)</h4>", unsafe_allow_html=True)
st.markdown("---")

# === API VƏ MODEL QURULUMU (Səhvsiz Versiya) ===
model = None # Başlanğıcda boş təyin edirik

try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # @st.cache_resource əlavə edirik ki, sayt hər tərpənəndə model yenidən yüklənməsin, Canavar daha sürətli hücum etsin!
        @st.cache_resource
        def load_model():
            return genai.GenerativeModel(
                model_name='gemini-1.5-pro', # Ən ağıllı Pro modeli!
                system_instruction=SYSTEM_INSTRUCTION
            )
        model = load_model()
    else:
        st.error("⚠️ GOOGLE_API_KEY 'Secrets' bölməsində tapılmadı! Zəhmət olmasa tənzimləmələri yoxla.")
        st.stop() # Açar yoxdursa kodu dayandırırıq ki, NameError xətası verməsin
except Exception as e:
    st.error(f"⚠️ API Xətası: {e}")
    st.stop() # Xəta varsa kodu dayandırırıq

# === YADDAŞ SİSTEMİ (Kontekst) ===
# Bu hissə botun əvvəlki yazılanları unutmaması üçündür
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# === GÖZ SİSTEMİ (Multimodallıq - Sidebar) ===
with st.sidebar:
    st.markdown("### 👁️ Canavarın Gözləri")
    st.info("Bura şəkil yüklə ki, A-ZEKA-ULTRA onu analiz etsin.")
    uploaded_file = st.file_uploader("Şəkil seç (JPG, PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Analiz üçün hazır", use_column_width=True)
    
    st.markdown("---")
    if st.button("Yaddaşı Sıfırla 🧹"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

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
user_input = st.chat_input("Əmrini ver, Abdullah... Canavarı sına!")

if user_input:
    # İstifadəçinin mesajını ekrana yaz
    with st.chat_message("user"):
        st.markdown(user_input)

    # Botun düşünmə prosesi
    with st.chat_message("assistant"):
        with st.spinner("A-ZEKA-ULTRA hədəfə kilitlənir... ⚡"):
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
                st.error("Nəsə xəta oldu. API limiti dolmuş və ya şəkil formatı dəstəklənməyə bilər.")
