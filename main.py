import streamlit as st
from groq import Groq

# 1. DÜNYA SƏVİYYƏLİ DİZAYN
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 15px; border: 1px solid #3e404b; }
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. GROQ SİSTEMİ (Sənin yeni gsk_... açarın buradadır)
# Bu açarı bura mən yerləşdirdim, heç nəyi dəyişmə.
client = Groq(api_key="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")

# 3. ULTRA BEYİN TƏLİMATI
system_prompt = """
Sən 'A-Zəka'-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb. 
Sən dünyanın ən sürətli və ağıllı Ultra Alimisən. 
Məqsədin bütün dünya üçün ən çətin sualları 1 saniyəyə həlli ilə cavablandırmaqdır.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. ƏSAS EKRAN
st.title("🧠 A-Zəka Ultra Alim")
st.markdown(f"**Yaradıcı:** Abdullah Mikayılov | **Sürət:** 1 san ⚡")

# Mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. SUAL QUTUSU
prompt = st.chat_input("Dahi alimə sualını ver...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Köhnə Gemini kodunu sildik, artıq rəsmi Groq mühərriki işləyir
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Bağlantı xətası! Zəhmət olmasa Planet VPN-i qoş və ya regionu (Almaniya) dəyiş.")
            st.info(f"Sistem mesajı: {str(e)}")
