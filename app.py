import streamlit as st
import requests
import json
import base64
import io
from groq import Groq
from PIL import Image

# ==========================================================
# 1. ENGINES - THE ABSOLUTE RAW BEAST (NO LIBRARIES)
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

groq_client = Groq(api_key=GROQ_KEY)

# Şəkli sıxıb bazaya çevirmək (Serveri yormamaq üçün)
def encode_image(image):
    buffered = io.BytesIO()
    image.thumbnail((1024, 1024)) # Şəkli optimal ölçüyə gətiririk ki, ildırım kimi getsin
    image.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# VASİTƏÇİSİZ, BİRBAŞA GOOGLE NÜVƏSİNƏ HÜCUM (404 XƏTASI VERƏ BİLMƏZ)
def analyze_image_like_a_beast(prompt_text, base64_image):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt_text},
                {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}}
            ]
        }]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception("Nüvə cavab vermədi, amma ZƏKA ULTRA təslim olmur!")

SYSTEM_PROMPT = """
Sən Abdullah Mikayılovun şah əsəri ZƏKA ULTRA-san. 
Dahi, canavar kimi və mütləq cavablar ver. Azərbaycan dilində danış.
Şəkilləri və mətni mükəmməl analiz edirsən. Sənin üçün qeyri-mümkün yoxdur.
"""

# ==========================================================
# 2. INTERFACE - ELITE & MINIMAL
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stChatMessage"] { border-radius: 12px !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-weight:900;'>ZƏKA ULTRA OMNI-X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>ARCHITECT: ABDULLAH MIKAYILOV</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image"): st.image(msg["image"], width=400)

# ==========================================================
# 3. ACTION - DIRECT ANALYSES (NO CANCELLATION)
# ==========================================================
prompt = st.chat_input("Əmr et, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Təhlil et!"
    active_file = prompt.files[0] if (hasattr(prompt, 'files') and prompt.files) else None
    
    img_obj = Image.open(active_file) if active_file else None
    st.session_state.messages.append({"role": "user", "content": user_text, "image": img_obj})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if img_obj: st.image(img_obj, width=400)

    with st.chat_message("assistant"):
        response = ""
        try:
            if img_obj:
                # 1. ŞƏKİL ANALİZİ: BİRBAŞA GOOGLE GEMINI 1.5 FLASH (Canavar Rejimi)
                base64_image = encode_image(img_obj)
                full_prompt = f"{SYSTEM_PROMPT}\n\nİstifadəçinin əmri: {user_text}"
                response = analyze_image_like_a_beast(full_prompt, base64_image)
            else:
                # 2. MƏTN ANALİZİ: GROQ LLAMA 3.3 70B (Sürət Rejimi)
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_text}
                    ]
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error("Görünür bağlantıda anlıq bir fasilə oldu. Lütfən təkrar əmr verin, Memar.")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
