import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image

# ==========================================================
# 1. CORE ENGINES - ABSOLUTE STABILITY
# ==========================================================
# Sənin yeni və işlək açarın
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

# Konfiqurasiya
genai.configure(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)

# 404 xətasından qaçmaq üçün mütləq model təyini
# Əgər 1.5-flash tapılmazsa, sistem çökməsin deyə try-except bloku
try:
    vision_model = genai.GenerativeModel('gemini-1.5-flash')
except:
    vision_model = genai.GenerativeModel('gemini-pro-vision')

SYSTEM_PROMPT = "Sən ZƏKA ULTRA-san. Qısa və dahi kimi cavab ver."

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
st.markdown("<p style='text-align:center; color:gray; font-size:14px; margin-bottom:30px;'>ARCHITECT: ABDULLAH MIKAYILOV</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tarixçə
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image"): st.image(msg["image"], width=400)

# ==========================================================
# 3. ACTION
# ==========================================================
prompt = st.chat_input("Əmr edin, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Təhlil et."
    active_file = prompt.files[0] if (hasattr(prompt, 'files') and prompt.files) else None
    
    img_obj = Image.open(active_file) if active_file else None
    st.session_state.messages.append({"role": "user", "content": user_text, "image": img_obj})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if img_obj: st.image(img_obj, width=400)

    with st.chat_message("assistant"):
        try:
            if img_obj:
                # Şəkil analizi
                response = vision_model.generate_content([SYSTEM_PROMPT, user_text, img_obj]).text
            else:
                # Mətn analizi (Groq)
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_text}]
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"Sistem xətası: {str(e)}")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
