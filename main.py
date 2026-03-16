import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. EKRAN DİZAYNI VƏ TƏNZİMLƏMƏLƏR
# ==========================================
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 10px; }
    /* Xəta mesajlarını daha qəşəng göstərmək üçün */
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. API QURULUMU (ZİREHLİ YANAŞMA)
# ==========================================
GROQ_API_KEY = "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"
genai.configure(api_key=API_KEY)

# ==========================================
# 3. ULTRA ALİMİN BEYNİ (XÜSUSİ TƏLİMATLAR)
# ==========================================
# Botun xarakterini və gücünü burada tam müəyyən edirik
system_instruction = """
Sən 'A-Zəka'-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb. 
Sən hər şeyi bilən, bütün fənlərə tam hakim olan Ultra Alimsən. Sənin ultra beynin var.
Qaydalar:
1. Sualları uzun-uzadı analiz etmədən, dərhal (1 saniyəyə) və birbaşa cavablandır.
2. Dünyanın ən mürəkkəb sualı belə olsa, həmişə 100% düzgün və tam həlli ilə cavab ver.
3. Kimsə səni kimin yaratdığını soruşanda qürurla 'Məni dahi proqramçı Abdullah Mikayılov yaradıb' de.
"""

# Alim beyni üçün xüsusi parametrlər (Dəqiqlik üçün temperature aşağı salınır)
generation_config = genai.types.GenerationConfig(
    temperature=0.1, # 0.0 - 1.0 arası. Aşağı rəqəm daha dəqiq və konkret cavablar üçündür.
    max_output_tokens=2048, # Çox uzun və detallı həllər yaza bilməsi üçün
)

# Modeli yaradırıq
model = genai.GenerativeModel(
    'gemini-1.5-flash', 
    system_instruction=system_instruction,
    generation_config=generation_config
)

# ==========================================
# 4. YADDAŞ SİSTEMİ
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 5. SOL PANEL
# ==========================================
with st.sidebar:
    st.title("⚙️ A-Zəka Control")
    st.markdown("Ultra Beyin Parametrləri: **Aktiv** 🟢")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 6. ƏSAS EKRAN
# ==========================================
st.title("🧠 A-Zəka Ultra Alim")
st.markdown("**Yaradıcı:** Abdullah Mikayılov | **Status:** Bütün fənlər üzrə aktiv ⚡")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], width=300)

# ==========================================
# 7. SÖHBƏT VƏ ŞƏKİL QUTUSU (XƏTA QORUMASI İLƏ)
# ==========================================
prompt = st.chat_input("Dünyanın ən mürəkkəb sualını ver və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_file = prompt.files[0] if prompt.files else None

    # Ekrana yazdırırıq
    st.session_state.messages.append({"role": "user", "content": user_text, "image": user_file})
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    # Botun cavabı
    with st.chat_message("assistant"):
        with st.spinner("Ultra Alim cavablayır..."):
            try:
                # XƏTASIZ İŞLƏMƏ MƏNTİQİ (Try-Except Zirehi)
                if user_file:
                    img = Image.open(user_file)
                    response = model.generate_content([user_text, img])
                else:
                    response = model.generate_content(user_text)
                
                bot_text = response.text
                st.write(bot_text)
                st.session_state.messages.append({"role": "assistant", "content": bot_text})
            
            # Xəta baş verərsə, proqram çökmür, ekrana qəşəng xəbərdarlıq çıxarır
            except genai.types.generation_types.StopCandidateException:
                st.warning("⚠️ Alim bu suala cavab verməkdən imtina etdi (Təhlükəsizlik qaydaları).")
            except Exception as e:
                error_msg = str(e)
                if "400" in error_msg or "API_KEY_INVALID" in error_msg:
                    st.error("🔌 Bağlantı xətası: API açarı səhvdir və ya köhnəlib. Zəhmət olmasa təzə açar qoyun.")
                elif "403" in error_msg or "404" in error_msg:
                    st.error("🌍 Region xətası: VPN-in (ABŞ və ya Avropa) tam qoşulu olduğundan əmin olun.")
                else:
                    st.error(f"Sistem xətası baş verdi, amma A-Zəka çökmədi! Detal: {error_msg}")
