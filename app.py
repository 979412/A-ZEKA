import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# ==========================================================
# 1. ENGINES - GROQ ULTRA SPEED (NO GOOGLE)
# ==========================================================
GROQ_KEY = "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"
groq_client = Groq(api_key=GROQ_KEY)

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

SYSTEM_PROMPT = """
Sən Abdullah Mikayılovun şah əsəri ZƏKA ULTRA-san. 
Dahi və mütləq cavablar ver. Azərbaycan dilində danış.
Şəkilləri və mətni mükəmməl analiz edirsən. Sənin üçün qeyri-mümkün yoxdur.
"""

# ==========================================================
# 2. INTERFACE - ELITE & MINIMAL
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

# CSS əlavəsi: Giriş sahəsinin həmişə görünməsi üçün
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stChatMessage"] { border-radius: 12px !important; }
    /* Chat inputun yerini bərkitmək üçün */
    .stChatInput {
        position: fixed;
        bottom: 30px;
        z-index: 1000;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-weight:900;'>ZƏKA ULTRA OMNI-X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>ARCHITECT: ABDULLAH MIKAYILOV</p>", unsafe_allow_html=True)

# Mesaj konteyneri (Yuxarıda mesajlar, aşağıda giriş sahəsi)
chat_container = st.container()

if "messages" not in st.session_state:
    st.session_state.messages = []

with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("image"): st.image(msg["image"], width=400)

# ==========================================================
# 3. ACTION - DIRECT ANALYSES
# ==========================================================
# accept_file=True hissəsi bəzi brauzerlərdə düyməni gizlədir, 
# ona görə bunu ən stabil halda saxlayırıq
prompt = st.chat_input("Əmr et, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Təhlil et!"
    active_file = prompt.files[0] if (hasattr(prompt, 'files') and prompt.files) else None
    
    img_obj = Image.open(active_file) if active_file else None
    st.session_state.messages.append({"role": "user", "content": user_text, "image": img_obj})
    
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_text)
            if img_obj: st.image(img_obj, width=400)

        with st.chat_message("assistant"):
            try:
                if img_obj:
                    base64_image = encode_image(img_obj)
                    chat_completion = groq_client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"{SYSTEM_PROMPT}\n\n{user_text}"},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}",
                                        },
                                    },
                                ],
                            }
                        ],
                        model="llama-3.2-90b-vision-preview",
                    )
                    response = chat_completion.choices[0].message.content
                else:
                    chat_comp = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": user_text}]
                    )
                    response = chat_comp.choices[0].message.content

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                st.error(f"Sistem xətası: {str(e)}")

# Avtomatik aşağı sürüşdürmə
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
