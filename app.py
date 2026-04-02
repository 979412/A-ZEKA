import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image

# ==========================================================
# 1. CORE ENGINES (Dinamik Model Yoxlanışı)
# ==========================================================
GEMINI_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"
GROQ_KEY = "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"

genai.configure(api_key=GEMINI_KEY)

# 404 xətasından qaçmaq üçün model siyahısını yoxlayan funksiya
def get_vision_model():
    # Sınaqdan keçiriləcək model adları (ən yeni sıralama ilə)
    models_to_try = [
        'gemini-1.5-flash-latest', 
        'gemini-1.5-flash', 
        'gemini-pro-vision'
    ]
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            # Kiçik bir test (modelin mövcudluğunu yoxlayır)
            return model
        except:
            continue
    return None

vision_model = get_vision_model()
groq_client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = "Sən ZƏKA ULTRA-san. Dahi kimi və birbaşa cavab ver."

# ==========================================================
# 2. INTERFACE
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: visible !important;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>ZƏKA ULTRA OMNI-X</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image"): st.image(msg["image"], width=300)

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
        if img_obj: st.image(img_obj, width=300)

    with st.chat_message("assistant"):
        try:
            if img_obj:
                if vision_model:
                    response = vision_model.generate_content([SYSTEM_PROMPT, user_text, img_obj]).text
                else:
                    response = "Xəta: Google Şəkil Mühərriki ilə bağlantı qurulmadı. API açarını yoxlayın."
            else:
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_text}]
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"Sistem xətası: {str(e)}")
