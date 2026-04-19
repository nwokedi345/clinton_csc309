import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import io

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="CSC 309 | Elite Voice Suite", page_icon="💖")

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
    /* Curvy Glassmorphism Text Area */
    .stTextArea textarea {
        border-radius: 30px !important;
        border: 2px solid #F06292 !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px); padding: 25px !important;
        font-size: 1.1rem !important;
    }
    /* Curvy Pink Buttons */
    div.stButton > button {
        background: linear-gradient(45deg, #D81B60, #EC407A) !important;
        color: white !important; border-radius: 50px !important;
        height: 3.5rem !important; width: 100%; font-weight: bold !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE MEMORY ---
if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""

# --- 3. UI LAYOUT ---
st.markdown('<h1 class="main-title">Voice AI Pad</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AD1457; font-weight:bold;'>Task 16 | Okoro Kelechi Clinton | 20231401932 .</p>", unsafe_allow_html=True)

lang_options = {"English": "en-US", "French": "fr-FR", "Igbo": "ig-NG"}
tts_langs = {"English": "en", "French": "fr", "Igbo": "ig"}
selected_lang = st.selectbox("🌍 Select Language", list(lang_options.keys()))

# --- 4. THE INPUT (SPEECH TO TEXT) ---
recorded_audio = st.audio_input("Record your voice")

if recorded_audio:
    try:
        # Convert and Process Audio
        audio_segment = AudioSegment.from_file(recorded_audio)
        buffer = io.BytesIO()
        audio_segment.export(buffer, format="wav")
        buffer.seek(0)

        r = sr.Recognizer()
        with sr.AudioFile(buffer) as source:
            audio_data = r.record(source)
            # Transcribe
            new_text = r.recognize_google(audio_data, language=lang_options[selected_lang])
            
            # THE FIX: Add new text to the existing session memory
            st.session_state.doc_text += f" {new_text.capitalize()}."
            st.toast("Transcribed!", icon="✅")
            
    except Exception as e:
        st.error("Wait, I didn't catch that. Please try speaking again!")

# Text Area tied to Session State
# Note: Any manual typing in this box will also be saved to doc_text
st.session_state.doc_text = st.text_area("Your Document", value=st.session_state.doc_text, height=300)

# --- 5. ACTION BUTTONS ---
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🗑️ Clear All"):
        st.session_state.doc_text = ""
        st.rerun()

with c2:
    if st.button("🔊 Read Aloud"):
        current_text = st.session_state.doc_text
        if current_text.strip():
            with st.spinner("Preparing Voice..."):
                tts = gTTS(text=current_text, lang=tts_langs[selected_lang])
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                st.audio(audio_fp, format="audio/mp3", autoplay=True)
        else:
            st.warning("The pad is empty! Record something first.")

with c3:
    st.download_button("📥 Save .txt", st.session_state.doc_text, file_name="dictation.txt")
