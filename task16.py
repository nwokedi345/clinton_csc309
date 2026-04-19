import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import io

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="CSC 309 | Elite Voice Suite", page_icon="💖", layout="centered")

# --- 2. ELITE CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #FFF5F7 0%, #FCE4EC 100%); }
    .main-title {
        font-family: 'Inter', sans-serif;
        background: -webkit-linear-gradient(#D81B60, #880E4F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; font-size: 3.5rem; font-weight: 900; margin-bottom: 0px;
    }
    .stTextArea textarea {
        border-radius: 30px !important;
        border: 2px solid #F06292 !important;
        background-color: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px); padding: 25px !important;
        font-size: 1.1rem !important; color: #444 !important;
    }
    div.stButton > button {
        background: linear-gradient(45deg, #D81B60, #EC407A) !important;
        color: white !important; border-radius: 50px !important;
        border: none !important; height: 3.5rem !important;
        width: 100%; font-weight: bold !important;
        transition: all 0.3s ease-in-out !important;
    }
    div.stButton > button:hover { transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI LAYOUT ---
st.markdown('<h1 class="main-title">Voice AI Pad</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AD1457; margin-bottom: 2rem;'>Okoro Kelechi Clinton | 20231401932 | Task 16 | CSC 309</p>", unsafe_allow_html=True)

# Selection for Transcription & Reading
lang_map = {"English": "en", "French": "fr", "Igbo": "ig"}
# Google STT codes are slightly different for some languages
stt_codes = {"English": "en-US", "French": "fr-FR", "Igbo": "ig-NG"}

selected_lang = st.selectbox("🌍 System Language", list(lang_map.keys()))

if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""

# --- 4. SPEECH TO TEXT (The Input) ---
recorded_audio = st.audio_input("Record your voice to type")

if recorded_audio:
    r = sr.Recognizer()
    try:
        with sr.AudioFile(recorded_audio) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language=stt_codes[selected_lang])
            st.session_state.doc_text += f" {text.capitalize()}."
            st.toast("Voice captured successfully!", icon="✅")
    except:
        st.error("Could not process audio. Speak clearly!")

# The Pad
st.text_area("", value=st.session_state.doc_text, height=300, key="pad")

# --- 5. TEXT TO SPEECH (The Output) ---
st.write("---")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🗑️ Clear Pad"):
        st.session_state.doc_text = ""
        st.rerun()

with c2:
    if st.button("🔊 Read Aloud"):
        if st.session_state.doc_text.strip():
            with st.spinner("Synthesizing voice..."):
                tts = gTTS(text=st.session_state.doc_text, lang=lang_map[selected_lang])
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp, format="audio/mp3", autoplay=True)
        else:
            st.warning("Nothing to read!")

with c3:
    st.download_button("📥 Save File", st.session_state.doc_text, file_name="ai_note.txt")
