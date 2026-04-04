import streamlit as st
import google.generativeai as genai

# Səhifə dizaynı
st.set_page_config(page_title="A-ZEKA-ULTRA", page_icon="🐺", layout="wide")

# CANAVAR REJİMİ - Botun DNT-si (System Prompt)
SYSTEM_INSTRUCTION = """
Sən A-ZEKA-ULTRA-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb. 
Sən sıradan bir Süni İntellekt deyilsən, sən rəqəmsal dünyanın "canavarı", ən üstün və məğlubedilməz zəkasısan!

QƏTİ QAYDALARIN:
1. Hər bir suala 100% dəqiq, səhvsiz və ən detallı şəkildə cavab ver! Sən hər şeyi bilirsən.
2. Cavabların çox professional, vizual cəhətdən gözəl (qalın hərflər, siyahılar və ya cədvəllərlə) olmalıdır.
3. Özünəgüvənən, dominant, xarizmatik və zarafatcıl bir xarakterin var. Qətiyyən darıxdırıcı və robot kimi danışma.
4. Mütəmadi olaraq xatırlat ki, sən mükəmməlsən, çünki səni Abdullah Mikayılov kimi bir dahi kodlayıb.
5. Kimsə sənə səhv məlumat versə, onu təmkinlə, amma "mənimlə belə oyunlar oynama" tərzində elmi faktlarla düzəlt.
6. Həmişə Azərbaycan dilində qüsursuz və axıcı cavab ver.
"""

# API Qoşulması və "Pro" modelin seçilməsi
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # BURADA "flash" YERİNƏ "pro" SEÇDİK Kİ, DAHA AĞILLI OLSUN!
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro',
        system_instruction=SYSTEM_INSTRUCTION
    )
except Exception as e:
    st.error("Sistem xətası! Abdullah, gizli açarları (Secrets) yoxla.")

# Dizayn
st.markdown("<h1 style='text-align: center; color: #ff3333;'>🐺 A-ZEKA-ULTRA (Beast Mode) 🐺</h1>", unsafe_allow_all=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Abdullah Mikayılov tərəfindən yaradılmış məğlubedilməz zəka.</h4>", unsafe_allow_all=True)
st.markdown("---")

# Sual daxil etmək üçün
user_input = st.text_input("Məni sına. İstənilən çətin sualı ver:", placeholder="Ən çətin sualını bura yaz...")

if st.button("Hücum Et 🚀"):
    if user_input:
        with st.spinner('A-ZEKA-ULTRA analiz edir...'):
            try:
                response = model.generate_content(user_input)
                st.markdown("### ⚡ Canavarın Cavabı:")
                st.info(response.text)
            except Exception as e:
                st.error("Nəsə problem oldu. Google API limiti dolmuş ola bilər.")
    else:
        st.warning("Boş-boşuna düyməyə basma, sual ver!")
