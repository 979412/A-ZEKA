import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image

# ==========================================================
# 1. CORE ENGINES - THE ABSOLUTE STABILITY
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

# Google AI Konfiqurasiyası
genai.configure(api_key=GEMINI_KEY)

# XƏTAYA QARŞI QALXAN: Model çağırışını funksiya daxilinə alırıq
def get_safe_vision_model():
    # İlk növbədə ən stabil adı yoxlayırıq
    try:
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        try:
            # Alternativ ad
            return genai.GenerativeModel('models/gemini-1.5-flash')
        except:
            # Ən son ehtiyat variant
            return genai.GenerativeModel('gemini-pro-vision')

vision_model = get_safe_vision_model()
groq_client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = """
Sən Abdullah Mikayılovun şah əsəri ZƏKA ULTRA-san. 
Dahi kimi cavab ver. Sənin lüğətində 'xəta' və ya 'bilmirəm' yoxdur.
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
    header {visibility: visible !important;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-weight:900;'>ZƏKA ULTRA OMNI-X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; font-size:14px; margin-bottom:20px;'>ARCHITECT: ABDULLAH MIKAYILOV</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], width=400)

# ==========================================================
# 3. ACTION LOGIC
# ==========================================================
prompt = st.chat_input("Əmr edin, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Təhlil et."
    active_file = prompt.files[0] if (hasattr(prompt, 'files') and prompt.files) else None
    
    img_obj = None
    if active_file:
        img_obj = Image.open(active_file)

    st.session_state.messages.append({"role": "user", "content": user_text, "image": img_obj})
    with st.chat_message("user"):
        st.markdown(user_text)
        if img_obj: st.image(img_obj, width=400)

    with st.chat_message("assistant"):
        try:
            if img_obj:
                # Şəkil analizi üçün birbaşa və təmiz çağırış
                response = vision_model.generate_content([SYSTEM_PROMPT, user_text, img_obj]).text
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
            # Xəta mesajını daha professional göstərək
            st.warning("Zəka Ultra mühərriki optimallaşdırılır... Zəhmət olmasa bir daha cəhd edin.")
            st.error(f"Texniki detal: {str(e)}")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
