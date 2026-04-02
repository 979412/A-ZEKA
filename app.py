import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image

# ==========================================================
# 1. ENGINES - YENİ API AÇARI İNTEQRASİYA EDİLDİ
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

# Google Generative AI tənzimləməsi
genai.configure(api_key=GEMINI_KEY)

# Modeli birbaşa adla çağırırıq (Xətadan qaçmaq üçün ən stabil yol)
vision_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = """
Sən Abdullah Mikayılovun şah əsəri ZƏKA ULTRA-san. 
Sənin biliyin mütləqdir. Qısa, dəqiq və dahi kimi cavab ver.
Məktəbdə hamını intellektinlə heyran qoy.
"""

# ==========================================================
# 2. ELITE INTERFACE
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    [data-testid="stChatMessage"] { 
        border-radius: 15px !important; 
        border: 1px solid #f0f2f6 !important; 
        box-shadow: 0 5px 15px rgba(0,0,0,0.02);
    }
    .mega-title { 
        font-size: 42px !important; 
        font-weight: 900; 
        text-align: center; 
        color: #000; 
        letter-spacing: -2px;
        margin-bottom: 0px;
    }
    footer {visibility: hidden;}
    header {visibility: visible !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='mega-title'>ZƏKA ULTRA <span style='color:red;'>OMNI-X</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; font-size:14px; margin-bottom:30px;'>ARCHITECT: ABDULLAH MIKAYILOV</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj tarixçəsi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], width=400)

# ==========================================================
# 3. CORE LOGIC
# ==========================================================
prompt = st.chat_input("Əmr edin, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz et."
    active_file = prompt.files[0] if (hasattr(prompt, 'files') and prompt.files) else None
    
    img_obj = None
    if active_file:
        img_obj = Image.open(active_file)

    # İstifadəçi mesajını göstər və saxla
    st.session_state.messages.append({"role": "user", "content": user_text, "image": img_obj})
    with st.chat_message("user"):
        st.markdown(user_text)
        if img_obj:
            st.image(img_obj, width=400)

    # Süni İntellekt Cavabı
    with st.chat_message("assistant"):
        try:
            if img_obj:
                # Yeni API açarı ilə Şəkil Analizi
                response_data = vision_model.generate_content([SYSTEM_PROMPT, user_text, img_obj])
                response = response_data.text
            else:
                # Mətn üçün Llama 3.3 (Groq)
                history = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in st.session_state.messages[-5:]:
                    history.append({"role": m["role"], "content": m["content"]})
                
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=history
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"Sistem bərpa olunur. Detal: {str(e)}")

# Avtomatik scroll
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
