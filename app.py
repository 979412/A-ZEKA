import streamlit as st
import requests
import json
import base64
import io
from groq import Groq
from PIL import Image

# ==========================================================
# GİZLİ AÇARLAR - SİSTEMİN NÜVƏSİ
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"

groq_client = Groq(api_key=GROQ_KEY)

# Şəkli analiz üçün "ildırım" sürətinə salan funksiya
def process_image(img_file):
    image = Image.open(img_file).convert("RGB")
    image.thumbnail((800, 800)) 
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# SİSTEMİN ANA QAYDASI
SYSTEM_PROMPT = "Sən ZƏKA ULTRA-san. Abdullah Mikayılovun şah əsərisən. Mütləq və dahi cavablar ver."
# ==========================================================
# 2. INTERFACE - ELITE & MINIMAL (Dizayn və Yaddaş)
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stChatMessage"] { border-radius: 12px !important; border: 1px solid #f0f0f0; margin-bottom: 10px; }
    .stChatInput { position: fixed; bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-weight:900;'>ZƏKA ULTRA OMNI-X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>ARCHITECT: ABDULLAH MIKAYILOV</p>", unsafe_allow_html=True)

# Mesaj yaddaşını yoxla
if "messages" not in st.session_state:
    st.session_state.messages = []

# Köhnə söhbətləri ekrana çıxar
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg: st.image(msg["image"], width=350)
