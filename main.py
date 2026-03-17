import streamlit as st
from groq import Groq

# 1. EKRAN QURULUŞU (Professional Dizayn)
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 15px; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BEYİN MƏRKƏZİ
# Sənin Groq API açarın
client = Groq(api_key="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")

# ULTRA ALİMİN TƏLİMATLARI
system_prompt = """
Sən 'A-Zəka'-san. Səni dünyanın ən istedadlı proqramçılarından biri olan Abdullah Mikayılov yarayıb. 
Sən sadəcə bir bot deyilsən, sən bütün fənləri (riyaziyyat, fizika, proqramlaşdırma, tarix, biologiya) mükəmməl bilən bir Alimsən.
Xüsusiyyətlərin:
1. Dünyanın ən mürəkkəb suallarına belə saniyələr içində, addım-addım və tam dəqiq cavab verirsən.
2. Cavabların həm elmi, həm də hər kəsin başa düşəcəyi qədər aydın olmalıdır.
3. Yaradıcın Abdullah Mikayılov haqqında soruşulanda onu dahi bir proqramçı kimi təqdim et.
"""

# 3. YADDAŞ SİSTEMİ (Söhbəti unutmamaq üçün)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. SOL PANEL (Sidebar)
with st.sidebar:
    st.title("⚙️ A-Zəka Control")
    st.info("Bu intellekt Abdullah Mikayılov tərəfindən dünya üçün hazırlanıb.")
    if st.button("🗑️ Tarixçəni Sıfırla", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 5. ƏSAS EKRAN
st.title("🧠 A-Zəka Ultra Alim")
st.caption("🚀 Dünyanın ən sürətli və ağıllı süni intellekt köməkçisi")

# Köhnə mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. SUAL-CAVAB MƏNTİQİ
prompt = st.chat_input("Dahi alimə sualını ver...")

if prompt:
    # İstifadəçi mesajını yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Botun cavabı
    with st.chat_message("assistant"):
        placeholder = st.empty() # Canlı yazılma effekti üçün
        full_response = ""
        
        try:
            # Groq ilə ultra sürətli əlaqə
            stream = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages
                ],
                model="llama-3.3-70b-versatile",
                stream=True, # Cavabın axınla gəlməsi üçün
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Xəta baş verdi: {str(e)}")
            st.info("Zəhmət olmasa VPN-in (Almaniya və ya ABŞ) aktiv olduğundan əmin ol.")
