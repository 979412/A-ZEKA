import streamlit as st
import requests
import base64

# 1. EKRAN DİZAYNI
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. API AÇARI - DİQQƏT: Yeni aldığın açarı bura yapışdır!
# Bura bir daha mesaj kimi açar göndərmə, sadəcə öz faylında dəyiş.
API_KEY = "AIzaSyDGICc3XJwxz4L_hlrdxb-Sog9ILawbmfk"

# 3. YADDAŞ SİSTEMİ
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. SOL PANEL
with st.sidebar:
    st.title("⚙️ A-Zəka Control")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 5. ƏSAS EKRAN
st.title("🧠 A-Zəka Ultra Alim")
st.markdown(f"**Yaradıcı:** Abdullah Mikayılov | **Status:** Aktiv ⚡")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], width=300)

# 6. GÜCLÜ BEYİN VƏ YAZI QUTUSU
prompt = st.chat_input("Dahi alimə sual ver və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_file = prompt.files[0] if prompt.files else None

    st.session_state.messages.append({"role": "user", "content": user_text, "image": user_file})
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka analiz edir..."):
            
            # Daha stabil olan v1 model ünvanı
           url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            
            system_instruction = "Sən 'A-Zəka'-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb. Sən hər şeyi bilən Ultra Alimsən. Sualları mütləq addım-addım və çox dəqiq izah etməlisən."
            
            parts = [{"text": f"{system_instruction}\n\nİstifadəçi sualı: {user_text}"}]
            
            if user_file:
                b64_image = base64.b64encode(user_file.getvalue()).decode('utf-8')
                parts.append({
                    "inline_data": {
                        "mimeType": user_file.type,
                        "data": b64_image
                    }
                })
            
            payload = {"contents": [{"parts": parts}]}
            
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    res_json = response.json()
                    bot_text = res_json['candidates'][0]['content']['parts'][0]['text']
                    st.write(bot_text)
                    st.session_state.messages.append({"role": "assistant", "content": bot_text})
                else:
                    st.error(f"Xəta: {response.status_code}")
                    # Əgər VPN işləmirsə və ya region problemi varsa, Google-un cavabını bura yazdırırıq:
                    st.warning("Google-dan gələn mesaj:")
                    st.json(response.json())
                    st.info("Məsləhət: VPN-in ABŞ və ya Avropa regionuna qoşulduğundan əmin ol.")
            except Exception as e:
                st.error(f"Bağlantı xətası: {e}")
