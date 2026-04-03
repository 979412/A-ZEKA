import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# ==========================================================
# 1. CORE ENGINE
# ==========================================================
GROQ_KEY = "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"
groq_client = Groq(api_key=GROQ_KEY)

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# ==========================================================
# 2. INTERFACE (MODERN & STABLE)
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA", layout="centered")

st.markdown("<h1 style='text-align:center;'>ZƏKA ULTRA OMNI-X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>ARCHITECT: ABDULLAH MIKAYILOV</p>", unsafe_allow_html=True)

# Şəkil yükləmə paneli (Həmişə görünən hissə)
uploaded_file = st.file_uploader("Şəkil yükləyin və ya bura sürükləyin", type=["jpg", "jpeg", "png"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj tarixçəsi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Mətn girişi
user_input = st.chat_input("Sualınızı bura yazın...")

# ==========================================================
# 3. ACTION LOGIC
# ==========================================================
if user_input:
    # İstifadəçi mesajını göstər
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                # ŞƏKİL ANALİZİ (GROQ VISION)
                img = Image.open(uploaded_file)
                base64_image = encode_image(img)
                
                completion = groq_client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": user_input},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }
                    ]
                )
                response = completion.choices[0].message.content
            else:
                # SADƏ MƏTN ANALİZİ
                chat_completion = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": user_input}]
                )
                response = chat_completion.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error("Mühərrikdə kiçik bir ləngimə oldu. Yenidən cəhd edin.")
