import streamlit as st
import google.generativeai as genai

# Səhifə tənzimləmələri
st.set_page_config(page_title="EduGenius AI", page_icon="🎓")

# Google Gemini-ni arxa fonda (gizli) qoşmaq
# Bu sətir Streamlit-in 'Secrets' bölməsindən açarı oxuyacaq
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Sistem qoşulmasında xəta var. Zəhmət olmasa Secrets bölməsini yoxlayın.")

# Sol panel (Yalnız rol seçimi)
with st.sidebar:
    st.title("⚙️ Seçimlər")
    role = st.radio("Siz kimsiniz?", ["Şagird", "Müəllim"])
    st.markdown("---")
    st.write("Yaradıcı: **Abdullah Mikayılov**")

# Əsas ekran
st.title("🎓 EduGenius AI")
st.write("### Məktəblilər və Müəllimlər üçün Süni İntellekt Sistemi")

user_input = st.text_input("Sualınızı bura yazın:")

if st.button("Cavablandır 🚀"):
    if user_input:
        with st.spinner('EduGenius düşünür...'):
            if role == "Müəllim":
                prompt = f"Sən peşəkar bir müəllimsən. Bu mövzu üçün dərs planı və testlər hazırla: {user_input}"
            else:
                prompt = f"Sən şagird dostusan. Bu mövzunu uşağa çox sadə izah et: {user_input}"
            
            response = model.generate_content(prompt)
            st.markdown("---")
            st.write(response.text)
    else:
        st.warning("Zəhmət olmasa sual yazın.")
