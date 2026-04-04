import streamlit as st
import google.generativeai as genai

# Səhifənin tənzimləmələri (Cəmi 1 dəfə yazılmalıdır)
st.set_page_config(page_title="EduGenius AI", page_icon="🎓")

# Sol tərəfdəki Ayarlar bölməsi
with st.sidebar:
    st.title("⚙️ Ayarlar")
    api_key = st.text_input("Google API Key daxil edin:", type="password")
    role = st.radio("Siz kimsiniz?", ["Şagird", "Müəllim"])
    st.markdown("---")
    st.write("Yaradıcı: **Abdullah Mikayılov**")

# Əsas ekran
st.title("🎓 EduGenius AI")
st.write("### Məktəblilər və Müəllimlər üçün Süni İntellekt Sistemi")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        user_input = st.text_input("Sualınızı və ya mövzunu bura yazın:")

        if st.button("Cavablandır 🚀"):
            if user_input:
                with st.spinner('EduGenius düşünür...'):
                    # Rol seçiminə görə xüsusi təlimat (Prompt)
                    if role == "Müəllim":
                        prompt = f"Sən peşəkar bir müəllimsən. Bu mövzu üçün ətraflı dərs planı və 5 ədəd maraqlı test sualı hazırla: {user_input}"
                    else:
                        prompt = f"Sən mehriban bir şagird dostusan. Bu mövzunu bir məktəbliyə çox sadə, maraqlı və aydın misallarla izah et: {user_input}"
                    
                    response = model.generate_content(prompt)
                    st.success(f"Budur, {role} üçün hazırladığım cavab:")
                    st.markdown("---")
                    st.write(response.text)
            else:
                st.warning("Zəhmət olmasa bir sual yazın.")
    except Exception as e:
        st.error(f"Xəta baş verdi: API açarı səhv ola bilər. Detal: {e}")
else:
    st.info("💡 Başlamaq üçün sol tərəfdəki panelə Google Gemini API Key-inizi daxil edin.")
