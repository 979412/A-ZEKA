import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image
import base64
import io

# ==========================================================
# 1. ENGINES - ULTRA POWER
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

genai.configure(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)

# Ən sürətli mühərriklər siyahısı
MODELS = ['gemini-1.5-flash', 'llama-3.2-90b-vision-preview']

SYSTEM_PROMPT = "Sən ZƏKA ULTRA-san. Qısa, dahi və canavar kimi cavab ver. Azərbaycan dilində danış."

# ==========================================================
# 2. INTERFACE - ELITE & CLEAN
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stChatMessage"] { border-radius: 10px !important; }
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
# 3. ACTION - INSTANT RESPONSE
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
                # 1. CƏHD: Google (İldırım sürəti ilə)
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    res = model.generate_content([SYSTEM_PROMPT, user_text, img_obj])
                    response = res.text
                except:
                    # 2. CƏHD: Groq (Əgər Google xəta versə, saniyə itirmədən bura keçir)
                    buffered = io.BytesIO()
                    img_obj.save(buffered, format="JPEG")
                    img_b64 = base64.b64encode(buffered.getvalue()).decode()
                    
                    chat_completion = groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": [{"type": "text", "text": user_text}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}]}],
                        model="llama-3.2-90b-vision-preview",
                    )
                    response = chat_completion.choices[0].message.content
            else:
                # Mətn söhbəti
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": user_text}]
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except:

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
