import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="CSC 309 | Elite Voice Suite", page_icon="💖")

# --- MAINTAINING THE PINK UI ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #FFF5F7 0%, #FCE4EC 100%); }
    .main-title {
        font-family: 'Inter', sans-serif;
        background: -webkit-linear-gradient(#D81B60, #880E4F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; font-size: 3.5rem; font-weight: 900;
    }
    .stTextArea textarea {
        border-radius: 30px !important;
        border: 2px solid #F06292 !important;
        background-color: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px); padding: 25px !important;
    }
    div.stButton > button {
        background: linear-gradient(45deg, #D81B60, #EC407A) !important;
        color: white !important; border-radius: 50px !important;
        height: 3.5rem !important; width: 100%; font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Voice AI Pad</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AD1457;'> Okoro Kelechi Clinton | 20231401932 | Task 16 | CSC 309</p>", unsafe_allow_html=True)

# Language Mappings
stt_codes = {"English": "en-US", "French": "fr-FR", "Igbo": "ig-NG"}
tts_codes = {"English": "en", "French": "fr", "Igbo": "ig"}
selected_lang = st.selectbox("🌍 System Language", list(stt_codes.keys()))

if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""

# --- THE FIX: AUDIO RECORDING & TRANSCRIPTION ---
recorded_audio = st.audio_input("Record your voice")

if recorded_audio:
    try:
        with st.spinner("✨ Cleaning audio & transcribing..."):
            # Step A: Convert the raw recording into a format Google understands
            audio_segment = AudioSegment.from_file(recorded_audio)
            buffer = io.BytesIO()
            audio_segment.export(buffer, format="wav")
            buffer.seek(0)

            # Step B: Transcribe
            r = sr.Recognizer()
            with sr.AudioFile(buffer) as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data, language=stt_codes[selected_lang])
                st.session_state.doc_text += f" {text.capitalize()}."
                st.toast("Captured!", icon="✅")
    except Exception as e:
        st.error("Transcription failed. Please check your internet or try speaking again.")

# Text Display
st.text_area("", value=st.session_state.doc_text, height=300, key="pad")

# --- ACTION BUTTONS ---
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🗑️ Clear"):
        st.session_state.doc_text = ""
        st.rerun()

with c2:
    if st.button("🔊 Read Aloud"):
        if st.session_state.doc_text.strip():
            tts = gTTS(text=st.session_state.doc_text, lang=tts_codes[selected_lang])
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            st.audio(fp, format="audio/mp3", autoplay=True)

with c3:
    st.download_button("📥 Save .txt", st.session_state.doc_text, file_name="ai_note.txt")
