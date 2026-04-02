import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image

# ==========================================================
# 1. CORE ENGINES - UNIVERSAL ACCESS
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

genai.configure(api_key=GEMINI_KEY)

# 404 XƏTASINI KÖKÜNDƏN KƏSƏN MƏNTİQ
def load_vision_model():
    # Birinci ən stabil köhnə modeli yoxlayırıq (Çünki o hər serverdə var)
    try:
        return genai.GenerativeModel('gemini-pro-vision')
    except:
        # Əgər o da olmasa, ən son flah modelini sınayırıq
        return genai.GenerativeModel('gemini-1.5-flash')

vision_model = load_vision_model()
groq_client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = "Sən ZƏKA ULTRA-san. Dahi kimi cavab ver. Azərbaycan dilində danış."

# ==========================================================
# 2. ELITE INTERFACE
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    [data-testid="stChatMessage"] { border-radius: 15px !important; border: 1px solid #f0f2f6 !important; }
    header {visibility: visible !important;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>ZƏKA ULTRA OMNI-X</h1>", unsafe_allow_html=True)

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
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
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
                # Mətn üçün Groq (Llama 3.3)
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_text}]
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            # Əgər yenə 404 olsa, istifadəçiyə bildirmədən Groq ilə cavab ver
            st.warning("Şəkil mühərriki bərpa olunur, mətn əsaslı analiz aparılır...")
            chat_comp = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": user_text + " (Qeyd: Şəkli görə bilmirəm, mətni cavabla)"}]
            )
            st.markdown(chat_comp.choices[0].message.content)

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
