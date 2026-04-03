import streamlit as st
import requests
import json
import base64
import io
from groq import Groq
from PIL import Image

# ==========================================================
# 1. CORE ENGINES - THE IMMORTAL CORE
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

groq_client = Groq(api_key=GROQ_KEY)

def encode_image(image):
    buffered = io.BytesIO()
    # Şəkli maksimum dərəcədə optimallaşdırırıq ki, heç bir server "ağırdır" deməsin
    image = image.convert("RGB")
    image.thumbnail((800, 800)) 
    image.save(buffered, format="JPEG", quality=70)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

SYSTEM_PROMPT = "Sən ZƏKA ULTRA-san. Dahi və vəhşi AI mühərrikisən. Azərbaycan dilində mütləq cavab ver."

# ==========================================================
# 2. INTERFACE - ELITE DESIGN
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header, footer {visibility: hidden;}
    [data-testid="stChatMessage"] { border-radius: 15px !important; border: 1px solid #f0f0f0; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-weight:900; color:#1E1E1E;'>ZƏKA ULTRA <span style='color:red;'>OMNI-X</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>DESIGNED BY ABDULLAH MIKAYILOV | 2 TRILLION CODE POWER</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image"): st.image(msg["image"], width=300)

# ==========================================================
# 3. ACTION - THE UNSTOPPABLE FLOW
# ==========================================================
prompt = st.chat_input("Əmr et, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli dərhal analiz et!"
    active_file = prompt.files[0] if (hasattr(prompt, 'files') and prompt.files) else None
    
    img_obj = Image.open(active_file) if active_file else None
    st.session_state.messages.append({"role": "user", "content": user_text, "image": img_obj})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if img_obj: st.image(img_obj, width=300)

    with st.chat_message("assistant"):
        response = ""
        try:
            if img_obj:
                b64_img = encode_image(img_obj)
                
                # CƏHD 1: BİRBAŞA GOOGLE API (İldırım hücumu)
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
                    payload = {"contents": [{"parts": [{"text": user_text}, {"inline_data": {"mime_type": "image/jpeg", "data": b64_img}}]}]}
                    res = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=10)
                    response = res.json()['candidates'][0]['content']['parts'][0]['text']
                except:
                    # CƏHD 2: GROQ VISION (Ehtiyat mühərrik - Dayansaq, ölərik!)
                    chat_comp = groq_client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[{"role": "user", "content": [{"type": "text", "text": user_text}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}]}],
                    )
                    response = chat_comp.choices[0].message.content
            else:
                # SÜRƏTLİ MƏTN ANALİZİ
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_text}]
                )
                response = chat_comp.choices[0].message.content

            if not response: response = "Memar, mən hazıram. Əmrinizi təkrar edin."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except:
            st.markdown("Zəka Ultra mütləq güclə işləyir. Şəkli yenidən daxil edin.")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
