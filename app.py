import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# ==========================================================
# 1. CORE ENGINES - GROQ UNIVERSAL STABILITY
# ==========================================================
GROQ_KEY = "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"
groq_client = Groq(api_key=GROQ_KEY)

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

SYSTEM_PROMPT = """
Sən Abdullah Mikayılovun şah əsəri ZƏKA ULTRA-san. 
Dahi və mütləq intellektlə cavab ver. Azərbaycan dilində danış.
"""

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
st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>ARCHITECT: ABDULLAH MIKAYILOV</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image"): st.image(msg["image"], width=400)

# ==========================================================
# 3. ACTION - MULTI-MODEL STABILITY SYSTEM
# ==========================================================
prompt = st.chat_input("Əmr edin, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz et."
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
                base64_image = encode_image(img_obj)
                # MODEL ADLARINI SIRAYLA YOXLAYAN "SMART-BYPASS" SİSTEMİ
                models_to_try = [
                    "llama-3.2-11b-vision-preview",
                    "llama-3.2-90b-vision-preview",
                    "llama-3.2-11b-vision-instruct",
                    "pixtral-12b-2409" # Ehtiyat variant
                ]
                
                for model in models_to_try:
                    try:
                        chat_completion = groq_client.chat.completions.create(
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"{SYSTEM_PROMPT}\n\n{user_text}"},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }],
                            model=model,
                        )
                        response = chat_completion.choices[0].message.content
                        if response: break
                    except:
                        continue
                
                if not response:
                    raise Exception("Bütün vizual mühərriklər sınaqdan keçdi, lakin server cavab vermədi.")
            else:
                # Mətn söhbəti (Ən stabil model: Llama 3.3 70B)
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_text}]
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"Sistem bərpa olunur. Detal: {str(e)}")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
