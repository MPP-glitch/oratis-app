import streamlit as st
import openai
import requests

st.set_page_config(page_title="Oratis", layout="centered")
st.title("Oratis – Coach IA Marcopolo")
st.write("Bienvenue dans Oratis, ton formateur IA qui t’aide à bien dire.")

# --- Fonction de synthèse vocale ElevenLabs ---
def jouer_voix_elevenlabs(texte):
    api_key = st.secrets["ELEVEN_API_KEY"]
    voice_id = "EXAVITQu4vr4xnSDxMaL"  # Rachel

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": texte,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        st.audio(response.content, format="audio/mp3")
    except:
        st.error("La voix d'Oratis n'a pas pu être générée.")

# --- Initialisation de session_state pour la simulation ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "step" not in st.session_state:
    st.session_state.step = 1
if "oratis_starts" not in st.session_state:
    st.session_state.oratis_starts = Fa
