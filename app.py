import streamlit as st
import requests
import json
import base64
from groq import Groq
from PIL import Image
import io

# ==========================================================
# 1. CORE ENGINES - RAW HTTP OVERRIDE
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

groq_client = Groq(api_key=GROQ_KEY)

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def call_gemini_raw(prompt_text, image_obj):
    # DİQQƏT: v1beta yox, birbaşa v1 stabil versiyasına müraciət edirik
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    image_base64 = encode_image(image_obj)
    
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt_text},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_base64
                    }
                }
            ]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Xəta buradakı 'status_code' hissəsində idi, düzəldildi:
    if response.status_code == 200:
        res_json = response.json()
        try:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        except:
            return "Analiz tamamlandı, lakin cavab formatlaşdırıla bilmədi."
    else:
        return f"Mühərrik cavab vermir (Kod: {response.status_code}). Detal: {response.text}"

SYSTEM_PROMPT = "Sən ZƏKA ULTRA-san. Dahi kimi cavab ver. Azərbaycan dilində danış."

# ==========================================================
# 2. ELITE INTERFACE
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    [data-testid="stChatMessage"] { border-radius: 15px !important; border: 1px solid #f0f2f6 !important; }
    footer {visibility: hidden;}
    header {visibility: visible !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-weight:900;'>ZƏKA ULTRA <span style='color:red;'>OMNI-X</span></h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image"): st.image(msg["image"], width=400)

# ==========================================================
# 3. ACTION
# ==========================================================
prompt = st.chat_input("Əmr edin, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli dərindən analiz et."
    active_file = prompt.files[0] if (hasattr(prompt, 'files') and prompt.files) else None
    
    img_obj = Image.open(active_file) if active_file else None
    st.session_state.messages.append({"role": "user", "content": user_text, "image": img_obj})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if img_obj: st.image(img_obj, width=400)

    with st.chat_message("assistant"):
        try:
            if img_obj:
                # RAW HTTP CALL
                with st.spinner("Zəka Ultra şəkli analiz edir..."):
                    response = call_gemini_raw(SYSTEM_PROMPT + " " + user_text, img_obj)
            else:
                # GROQ CALL
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_text}]
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"Kritik Xəta: {str(e)}")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
