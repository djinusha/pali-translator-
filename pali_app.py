import streamlit as st
import google.generativeai as genai

# ඔබගේ නවතම API Key එක
API_KEY = "AIzaSyCZbfdn_rHP3FV6Rh2zNMZjGNIns9w6kCE"
genai.configure(api_key=API_KEY)

def get_available_model():
    """ඔබේ ගිණුමට ලබාගත හැකි හොඳම model එක සොයා දෙයි"""
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # ප්‍රමුඛතාවය අනුව පරීක්ෂා කරයි
    for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
        if preferred in available_models:
            return preferred
    return available_models[0] if available_models else None

# UI සැකසුම
st.set_page_config(page_title="AI පාලි පරිවර්තකය", page_icon="☸️")
st.title("☸️ AI පාලි පරිවර්තකය")

try:
    working_model_name = get_available_model()
    if working_model_name:
        model = genai.GenerativeModel(working_model_name)
        st.success(f"පද්ධතිය සක්‍රීයයි (Model: {working_model_name})")
    else:
        st.error("කිසිදු Model එකක් හමු නොවීය. කරුණාකර API Key එක පරීක්ෂා කරන්න.")
except Exception as e:
    st.error(f"සම්බන්ධ වීමේ දෝෂයක්: {e}")

pali_text = st.text_area("පාලි වාක්‍යය මෙහි ඇතුළත් කරන්න:", placeholder="උදා: Sabbe satta bhavantu sukhitatta")

if st.button("පරිවර්තනය කරන්න"):
    if pali_text:
        with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
            try:
                prompt = f"Translate this Pali text to Sinhala and English, and provide a word-by-word breakdown: {pali_text}"
                response = model.generate_content(prompt)
                st.markdown("### 📝 ප්‍රතිඵලය:")
                st.write(response.text)
            except Exception as e:
                st.error(f"පරිවර්තනය කිරීමේදී දෝෂයක් සිදු විය: {e}")
    else:
        st.warning("කරුණාකර පාලි වාක්‍යයක් ඇතුළත් කරන්න.")