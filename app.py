import streamlit as st
import requests
import json
import base64
import io
from groq import Groq
from PIL import Image

# ==========================================================
# 1. CORE ENGINES - THE SUPREME CORE
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

groq_client = Groq(api_key=GROQ_KEY)

def encode_image(image):
    buffered = io.BytesIO()
    image = image.convert("RGB")
    # Şəkli çox kiçik ölçüyə salırıq ki, analiz ildırım kimi olsun
    image.thumbnail((512, 512)) 
    image.save(buffered, format="JPEG", quality=60)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

SYSTEM_PROMPT = "Sən ZƏKA ULTRA-san. Abdullah Mikayılovun qurduğu ən güclü AI-san. Analiz et və dahi kimi cavab ver."

# ==========================================================
# 2. INTERFACE - ELITE BLACK & WHITE
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header, footer {visibility: hidden;}
    [data-testid="stChatMessage"] { border-radius: 10px !important; border: 1px solid #eeeeee; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-weight:900;'>ZƏKA ULTRA OMNI-X</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image"): st.image(msg["image"], width=300)

# ==========================================================
# 3. ACTION - THE UNSTOPPABLE ANALYZER
# ==========================================================
prompt = st.chat_input("Əmr et, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Təhlil et."
    active_file = prompt.files[0] if (hasattr(prompt, 'files') and prompt.files) else None
    
    img_obj = Image.open(active_file) if active_file else None
    st.session_state.messages.append({"role": "user", "content": user_text, "image": img_obj})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if img_obj: st.image(img_obj, width=300)

    with st.chat_message("assistant"):
        response = ""
        # 1. CƏHD: GOOGLE GEMINI (BİRBAŞA NÜVƏ)
        if img_obj:
            b64_img = encode_image(img_obj)
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
                payload = {"contents": [{"parts": [{"text": user_text}, {"inline_data": {"mime_type": "image/jpeg", "data": b64_img}}]}]}
                res = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=15)
                response = res.json()['candidates'][0]['content']['parts'][0]['text']
            except:
                # 2. CƏHD: GROQ (ƏGƏR GOOGLE ÖLSƏ)
                try:
                    chat_comp = groq_client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[{"role": "user", "content": [{"type": "text", "text": user_text}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}]}],
                    )
                    response = chat_comp.choices[0].message.content
                except:
                    response = "Analiz uğursuz oldu, amma ZƏKA ULTRA yenidən yoxlayır. Lütfən şəkli bir daha atın."
        else:
            # SADƏ MƏTN
            chat_comp = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": user_text}]
            )
            response = chat_comp.choices[0].message.content

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
