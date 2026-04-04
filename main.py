import streamlit as st
import google.generativeai as genai

# Səhifənin dizaynı
st.set_page_config(page_title="EduGenius AI", page_icon="🎓")
st.title("🎓 EduGenius AI")
st.subheader("Məktəblilər və Müəllimlər üçün Süni İntellekt")

# Yan menyuda API Key girişi (Təhlükəsizlik üçün)
with st.sidebar:
    api_key = st.text_input("Google API Key daxil edin:", type="password")
    role = st.selectbox("Kimsiniz?", ["Şagird", "Müəllim"])

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    user_input = st.text_area("Sualınızı və ya mövzunu yazın:")

    if st.button("Cavablandır"):
        if user_input:
            with st.spinner('Düşünürəm...'):
                if role == "Müəllim":
                    prompt = f"Sən peşəkar müəllimsən. Bu mövzu üçün dərs planı və 5 suallıq test yarat: {user_input}"
                else:
                    prompt = f"Sən mehriban bir repetitorsan. Bu mövzunu 12 yaşlı uşağa izah edən kimi sadə izah et: {user_input}"
                
                response = model.generate_content(prompt)
                st.markdown("### 🤖 EduGenius-un Cavabı:")
                st.write(response.text)
        else:
            st.warning("Zəhmət olmasa bir mövzu daxil edin.")
else:
    st.info("Başlamaq üçün sol tərəfə API açarınızı daxil edin.")
