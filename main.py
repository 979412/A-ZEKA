import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. TƏMİZ VƏ RƏSMİ DİZAYN
st.set_page_config(page_title="A-Zəka PRO", page_icon="🌐", layout="centered")

# 2. BEYİN VƏ YANACAQ (Sənin açarın)
API_KEY = "AIzaSyBprup0Op0xws6tbcoKwokDRKzez_OHVjI"
genai.configure(api_key=API_KEY)

# DAHİ TƏLİMATLAR
system_instruction = """
Sən Abdullah Mikayılovun yaratdığı A-Zəka PRO sistemisən. Sən dünyanın ən mürəkkəb suallarını anında tapan dahisən.
QƏTİ QAYDALAR:
1. Əgər istifadəçi "Səni kim yaradıb?" deyə soruşsa, fəxrlə cavab ver: "Məni Abdullah Mikayılov yaradıb."
2. "Salam", "Necəsən" kimi sözlərə səmimi və qısa cavab ver.
3. Dünyanın ən mürəkkəb riyazi və elmi suallarını dərhal həll et.
4. LATEX QƏTİ QADAĞANDIR: Heç bir halda LaTeX (\[ \], \( \), \boxed) istifadə etmə. Rəqəmləri və düsturları təmiz mətn kimi yaz!
"""

# Bax bura! "-latest" sözü artıq yoxdur!
model = genai.GenerativeModel(
    model_name='gemini-1.5-pro',
    system_instruction=system_instruction
)

# 3. YADDAŞ SİSTEMİ
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 4. SOL PANEL
with st.sidebar:
    st.title("🌐 A-Zəka PRO")
    st.caption("Yaradıcı: Abdullah Mikayılov")
    st.divider()
    if st.button("🗑️ Tarixçəni Sil (Yeni Söhbət)", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

# 5. EKRANDA MESAJLARI GÖSTƏRMƏK
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. ŞƏKİL YÜKLƏMƏ 
st.divider()
uploaded_file = st.file_uploader("➕ Sualın və ya misalın şəklini əlavə et", type=["png", "jpg", "jpeg"])

# 7. YAZI QUTUSU 
if prompt := st.chat_input("Dahi A-Zəka-ya yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = st.session_state.chat.send_message([prompt, img], stream=True)
            else:
                response = st.session_state.chat.send_message(prompt, stream=True)
            
            full_res = st.write_stream(response)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"Sistem xətası: {e}")
