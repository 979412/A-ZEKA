import streamlit as st
import google.generativeai as genai

# Səhifənin başlığı
st.set_page_config(page_title="EduGenius AI", page_icon="🎓")
st.title("🎓 EduGenius AI")
st.write("Məktəblilər və Müəllimlər üçün Süni İntellekt Sistemi")

# API Key daxil etmək üçün yer
with st.sidebar:
    st.title("Ayarlar")
    api_key = st.text_input("Google API Key-i bura yazın:", type="password")
    role = st.radio("Siz kimsiniz?", ["Şagird", "Müəllim"])

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        user_input = st.text_input("Sualınızı bura yazın:")

        if st.button("Cavab Al"):
            if user_input:
                with st.spinner('Düşünürəm...'):
                    if role == "Müəllim":
                        prompt = f"Sən peşəkar müəllimsən. Bu mövzu üçün dərs planı və 5 test sualı yarat: {user_input}"
                    else:
                        prompt = f"Sən şagird dostusan. Bu mövzunu uşağa izah edən kimi çox sadə izah et: {user_input}"
                    
                    response = model.generate_content(prompt)
                    st.success("Budur:")
                    st.write(response.text)
            else:
                st.warning("Zəhmət olmasa sual yazın.")
    except Exception as e:
        st.error(f"Xəta baş verdi: {e}")
else:
    st.info("Sol tərəfdəki panelə API Key daxil edin ki, intellekt işə düşsün.")
