import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image

# ==========================================================
# 1. CORE ENGINES (IRONCLAD CONFIG)
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

genai.configure(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = """
Sən Abdullah Mikayılovun şah əsəri ZƏKA ULTRA-san. 
Dahi kimi cavab ver. Şəkilləri və mətni mükəmməl analiz edirsən.
Azərbaycan dilində ən yüksək səviyyədə cavab ver.
"""

# ==========================================================
# 2. INTERFACE
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

st.markdown("<h1 style='text-align:center; font-weight:900;'>ZƏKA ULTRA <span style='color:red;'>OMNI-X</span></h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image"): st.image(msg["image"], width=400)

# ==========================================================
# 3. SMART ANALYZER
# ==========================================================
prompt = st.chat_input("Əmr edin, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu faylı analiz et."
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
                # MODEL ADLARINI SIRAYLA YOXLAYAN MÜHƏRRİK
                for model_name in ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro-vision']:
                    try:
                        temp_model = genai.GenerativeModel(model_name)
                        res_obj = temp_model.generate_content([SYSTEM_PROMPT, user_text, img_obj])
                        response = res_obj.text
                        if response: break # Cavab gəldisə dayandır
                    except Exception:
                        continue # Xəta olsa növbəti modeli yoxla
                
                if not response:
                    raise Exception("Bütün şəkil mühərrikləri məşğuldur.")
            else:
                # Mətn üçün Groq
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_text}]
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.warning("Mühərrik daxili optimallaşdırma aparır, təkrar cəhd edin.")
            st.error(f"Xəta kodu: {str(e)}")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
