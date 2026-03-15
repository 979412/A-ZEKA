import streamlit as st
import requests
import base64

# 1. EKRAN DİZAYNI
st.set_page_config(page_title="A-Zəka | Ultra Alim", page_icon="🧠", layout="wide")

# 2. API AÇARI (Bura öz açarını daxil et)
API_KEY = "SƏNİN_API_AÇARIN" 
API_KEY = "AIzaSyBprup0Op0xws6tbcoKwokDRKzez_OHVjI"
# 3. SOL PANEL: BEYİN SEÇİCİ
with st.sidebar:
    st.title("⚙️ İdarəetmə Paneli")
    st.markdown("Xəta yoxdur, sadəcə birbaşa bağlantı!")
    
    secilen_beyin = st.selectbox(
        "Aktiv Beyni Seç:",
        [
            "gemini-1.5-flash",     # Şimşək sürətli (İlk bunu yoxla)
            "gemini-1.5-pro",       # Ən güclü ultra alim
            "gemini-pro"            # Köhnə baza
        ]
    )
    
    st.markdown("---")
    if st.button("🗑️ Tarixçəni Sil", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 4. ƏSAS EKRAN
st.title("🧠 A-Zəka Ultra Alim")
st.caption(f"Yaradıcı: Abdullah Mikayılov | Xətasız Birbaşa Bağlantı | Beyin: {secilen_beyin}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("image_url"): # Şəkli bazada göstəririk
            st.image(msg["image_url"], width=300)

# 5. YAZI QUTUSU (Şəkil dəstəkli)
prompt = st.chat_input("Dahi alimə ən çətin sualını ver və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_file = prompt.files[0] if prompt.files else None

    # İstifadəçi mesajını ekrana çıxarırıq
    st.session_state.messages.append({"role": "user", "content": user_text, "image_url": user_file})
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    # BOTUN CAVABI (Birbaşa REST API ilə)
    with st.chat_message("assistant"):
        with st.spinner("Birbaşa Google serverinə qoşulur (Donmaq yoxdur!)..."):
            
            # Google API URL-i
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{secilen_beyin}:generateContent?key={API_KEY}"
            
            # Ultra Alim Təlimatı
            telimat = "Sən 'A-Zəka'-san. Səni Abdullah Mikayılov yaradıb. Hər şeyi bilən Ultra Alimsən. Sualların həllini addım-addım və çox dəqiq izah et."
            
            # Mesajın Mətni
            parts = [{"text": user_text}]
            
            # Əgər şəkil varsa, onu şifrələyib göndəririk (Base64)
            if user_file:
                b64_sekil = base64.b64encode(user_file.getvalue()).decode('utf-8')
                parts.append({
                    "inline_data": {
                        "mimeType": user_file.type,
                        "data": b64_sekil
                    }
                })
            
            # Göndəriləcək Tam Paket
            payload = {
                "systemInstruction": {
                    "parts": [{"text": telimat}]
                },
                "contents": [
                    {
                        "role": "user",
                        "parts": parts
                    }
                ]
            }
            
            try:
                # İnternet sorğusu göndəririk (gRPC çökmələrini ləğv etdik!)
                response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
                
                # Əgər uğurludursa
                if response.status_code == 200:
                    bot_cavabi = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.write(bot_cavabi)
                    st.session_state.messages.append({"role": "assistant", "content": bot_cavabi})
                else:
                    # Əgər xəta varsa (404, 403 və s.), ekrana SƏBƏBİNİ yazdırırıq
                    st.error(f"❌ XƏTA KODU: {response.status_code}\n\nGoogle-un cavabı: {response.text}")
                    
            except Exception as e:
                st.error(f"İnternet bağlantısı kəsildi: {e}")
