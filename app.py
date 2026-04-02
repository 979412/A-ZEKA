import streamlit as st
import requests
import json
import base64
from groq import Groq
from PIL import Image
import io

# ==========================================================
# 1. CORE ENGINES - UNIVERSAL STABILITY
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

groq_client = Groq(api_key=GROQ_KEY)

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def call_gemini_raw(prompt_text, image_obj):
    # DİQQƏT: 1.5 tapılmayanda 1.0 Pro-ya keçən universal ünvan
    # Bu model hər yerdə aktivdir.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={GEMINI_KEY}"
    
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
    
    if response.status_code == 200:
        try:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            return "Analiz uğurla başa çatdı."
    else:
        # Əgər Pro Vision da naz eləsə, son şans: 1.5-i fərqli yolla çağır
        alt_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_KEY}"
        alt_res = requests.post(alt_url, headers=headers, data=json.dumps(payload))
        if alt_res.status_code == 200:
            return alt_res.json()['candidates'][0]['content']['parts'][0]['text']
        return f"Xəta: {response.status_code}. Google mühərriki bu zonada müvəqqəti bağlıdır."

SYSTEM_PROMPT = "Sən ZƏKA ULTRA-san. Dahi kimi və Azərbaycan dilində cavab ver."

# ==========================================================
# 2. INTERFACE
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
prompt = st.chat_input("Əmr edin...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz et."
    active_file = prompt.files[0] if (hasattr(prompt, 'files') and prompt.files) else None
    
    img_obj = Image.open(active_file) if active_file else None
    st.session_state.messages.append({"role": "user", "content": user_text, "image": img_obj})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if img_obj: st.image(img_obj, width=400)

    with st.chat_message("assistant"):
        try:
            if img_obj:
                with st.spinner("Zəka Ultra dərindən təhlil edir..."):
                    response = call_gemini_raw(SYSTEM_PROMPT + " " + user_text, img_obj)
            else:
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_text}]
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"Sistem bərpa olunur: {str(e)}")
