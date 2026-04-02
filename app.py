import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image
import io

# ==========================================================
# 1. CORE ENGINES - THE FINAL STABILITY
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

# Google Konfiqurasiyası
genai.configure(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)

# Bu model adı Google-un ən son və ən stabil ünvanıdır
# 'models/' prefiksi bəzi serverlərdə 404-ün qarşısını alır
VISION_MODEL_NAME = 'models/gemini-1.5-flash-latest'

SYSTEM_PROMPT = "Sən ZƏKA ULTRA-san. Dahi kimi Azərbaycan dilində cavab ver."

# ==========================================================
# 2. ELITE INTERFACE
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: visible !important;}
    footer {visibility: hidden;}
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
# 3. ACTION LOGIC
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
                # GOOGLE VISION - ƏN SON STABİL METOD
                model = genai.GenerativeModel(model_name=VISION_MODEL_NAME)
                # Şəkli birbaşa göndəririk (v1beta-dan qaçırıq)
                response_obj = model.generate_content([SYSTEM_PROMPT, user_text, img_obj])
                response = response_obj.text
            else:
                # GROQ TEXT - Llama 3.3
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_text}]
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            # Əgər hələ də 404 olsa, sistem çökməsin, mətni Groq-a yönləndir
            st.warning("Şəkil mühərriki regional blokdadır. Mətn əsaslı cavab hazırlanır...")
            chat_comp = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"İstifadəçi şəkil göndərdi, amma mən görə bilmirəm. Bu mətni cavabla: {user_text}"}]
            )
            fallback_res = chat_comp.choices[0].message.content
            st.markdown(fallback_res)
            st.error(f"Texniki Detal: {str(e)}")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
