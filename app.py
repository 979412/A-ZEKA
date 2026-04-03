import streamlit as st
import requests
import json
import base64
import io
from groq import Groq
from PIL import Image

# ==========================================================
# GİZLİ AÇARLAR - SİSTEMİN NÜVƏSİ
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

groq_client = Groq(api_key=GROQ_KEY)

# Şəkli analiz üçün "ildırım" sürətinə salan funksiya
def process_image(img_file):
    image = Image.open(img_file).convert("RGB")
    image.thumbnail((800, 800)) 
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# SİSTEMİN ANA QAYDASI
SYSTEM_PROMPT = "Sən ZƏKA ULTRA-san. Abdullah Mikayılovun şah əsərisən. Mütləq və dahi cavablar ver."
# ==========================================================
# 2. INTERFACE - ELITE & MINIMAL (Dizayn və Yaddaş)
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stChatMessage"] { border-radius: 12px !important; border: 1px solid #f0f0f0; margin-bottom: 10px; }
    .stChatInput { position: fixed; bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-weight:900;'>ZƏKA ULTRA OMNI-X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>ARCHITECT: ABDULLAH MIKAYILOV</p>", unsafe_allow_html=True)

# Mesaj yaddaşını yoxla
if "messages" not in st.session_state:
    st.session_state.messages = []

# Köhnə söhbətləri ekrana çıxar
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg: st.image(msg["image"], width=350)
            # ==========================================================
# 3. ACTION - THE UNSTOPPABLE ANALYZER (Mütləq Hücum)
# ==========================================================
prompt = st.chat_input("Əmr et, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz et!"
    st.session_state.messages.append({"role": "user", "content": user_text})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        
        # Şəkli yaddaşa al və ekrana ver
        active_img = None
        if prompt.files:
            active_img = Image.open(prompt.files[0])
            st.image(active_img, width=350)
            st.session_state.messages[-1]["image"] = active_img

    # ANALİZ PROSESİ - GERİ ÇƏKİLMƏK YOXDUR!
    with st.chat_message("assistant"):
        with st.spinner("ZƏKA ULTRA DÜŞÜNÜR..."):
            try:
                if active_img:
                    # ŞƏKİL ANALİZİ (İldırım Hücumu)
                    b64_data = process_image(prompt.files[0])
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
                    payload = {
                        "contents": [{
                            "parts": [
                                {"text": f"{SYSTEM_PROMPT}\n\nƏmr: {user_text}"},
                                {"inline_data": {"mime_type": "image/jpeg", "data": b64_data}}
                            ]
                        }]
                    }
                    res = requests.post(url, json=payload, timeout=20)
                    
                    if res.status_code == 200:
                        ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                    else:
                        # Ehtiyat: Groq Vision
                        chat_comp = groq_client.chat.completions.create(
                            model="llama-3.2-11b-vision-preview",
                            messages=[{"role": "user", "content": [
                                {"type": "text", "text": user_text},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}}
                            ]}]
                        )
                        ans = chat_comp.choices[0].message.content
                else:
                    # SADƏ MƏTN ANALİZİ
                    chat_comp = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": user_text}]
                    )
                    ans = chat_comp.choices[0].message.content

                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})

            except:
                st.markdown("ZƏKA ULTRA mütləq güclə işləyir. Bir daha əmr verin, Memar!")

# Avtomatik aşağı sürüşmə
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
