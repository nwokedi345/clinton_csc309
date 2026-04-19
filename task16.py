import streamlit as st
import speech_recognition as sr
import io

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="CSC 309 | Elite AI Pad", page_icon="💖", layout="centered")

# --- 2. ELITE CSS CUSTOMIZATION ---
st.markdown("""
    <style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #FFF5F7 0%, #FCE4EC 100%);
    }

    /* Title Styling */
    .main-title {
        font-family: 'Inter', sans-serif;
        background: -webkit-linear-gradient(#D81B60, #880E4F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0px;
    }

    /* Curvy Glassmorphism Text Area */
    .stTextArea textarea {
        border-radius: 30px !important;
        border: 2px solid #F06292 !important;
        background-color: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px);
        padding: 25px !important;
        font-size: 1.1rem !important;
        color: #444 !important;
        box-shadow: 0 10px 30px rgba(216, 27, 96, 0.1);
    }

    /* Pulse Animation for Recording */
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(216, 27, 96, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba(216, 27, 96, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(216, 27, 96, 0); }
    }

    /* Ultra Curvy Pink Buttons */
    div.stButton > button {
        background: linear-gradient(45deg, #D81B60, #EC407A) !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        height: 3.5rem !important;
        width: 100%;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 15px rgba(216, 27, 96, 0.3) !important;
        transition: all 0.3s ease-in-out !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(216, 27, 96, 0.4) !important;
    }

    /* Pulsing mic indicator style */
    .mic-active {
        color: #D81B60;
        font-weight: bold;
        animation: pulse 1.5s infinite;
        text-align: center;
        padding: 10px;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI LAYOUT ---
st.markdown('<h1 class="main-title">AI Voice Pad</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AD1457; margin-bottom: 2rem;'>Okoro Kelechi Clinton | 20231401932 | Task 16 | CSC 309</p>", unsafe_allow_html=True)

# Language Logic
lang_map = {"English": "en-US", "French": "fr-FR", "Igbo": "ig-NG"}
selected_lang = st.selectbox("🌍 Select Language", list(lang_map.keys()))

# Session State for Text
if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""

# Audio Input (Streamlit's newest native recording widget)
recorded_audio = st.audio_input("Record your voice here")

# --- 4. TRANSCRIPTION LOGIC ---
if recorded_audio:
    st.markdown('<div class="mic-active">✨ Processing your speech...</div>', unsafe_allow_html=True)
    
    r = sr.Recognizer()
    try:
        with sr.AudioFile(recorded_audio) as source:
            audio_data = r.record(source)
            # Using Google's free Web API
            text = r.recognize_google(audio_data, language=lang_map[selected_lang])
            st.session_state.doc_text += f" {text.capitalize()}."
            st.success("Captured!")
    except Exception as e:
        st.error("Couldn't hear that clearly. Try again!")

# Big Text Area
st.text_area("", value=st.session_state.doc_text, height=350, placeholder="Your transcribed text will appear here...")

# --- 5. COOL ACTION BUTTONS ---
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    if st.button("🗑️ Clear"):
        st.session_state.doc_text = ""
        st.rerun()

with c2:
    # Copying is a bit tricky in Streamlit, so we provide a quick select view
    st.button("📋 Ready to Copy")

with c3:
    st.download_button("📥 Save .txt", st.session_state.doc_text, file_name="my_dictation.txt")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>Powered by OpenAI Whisper & Google Speech API</p>", unsafe_allow_html=True)