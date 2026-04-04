import google.generativeai as genai
import os

# 1. AI-ni sazlayırıq
# QEYD: API açarını bura birbaşa yazmaq təhlükəlidir, amma test üçün hələlik belə edək.
API_KEY = "BURA_API_KEY_YAZILACAQ" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def edu_genius_beyin(sorğu, rol="şagird"):
    if rol == "müəllim":
        sistem_mesaji = f"Sən peşəkar bir müəllimsən. Bu mövzuda dərs planı və test hazırla: {sorğu}"
    else:
        sistem_mesaji = f"Sən şagirdlərin ən yaxşı dostusan. Bu mövzunu uşaqlara çox sadə dildə izah et: {sorğu}"
    
    response = model.generate_content(sistem_mesaji)
    return response.text

# Test edirik:
print("--- EduGenius İşə Düşdü ---")
print(edu_genius_beyin("Fotosintez nədir?", rol="şagird"))
