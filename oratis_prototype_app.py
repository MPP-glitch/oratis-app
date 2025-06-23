
import streamlit as st
import openai
import requests

st.title("Oratis – Coach IA Marcopolo")
st.write("Bienvenue dans Oratis, ton formateur IA qui t’aide à bien dire.")

# Fonction voix ElevenLabs
def jouer_voix_elevenlabs(texte):
    api_key = st.secrets["ELEVEN_API_KEY"]
    voice_id = "EXAVITQu4vr4xnSDxMaL"  # Voix Rachel

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

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        audio_bytes = response.content
        st.audio(audio_bytes, format="audio/mp3")
    else:
        st.error("La voix d'Oratis n'a pas pu être générée.")

# Phase 1 : Demande utilisateur
st.header("1. Pose ta question")
user_question = st.text_input("Quel est ton besoin ? (ex: Comment recadrer un collaborateur ?)")

if user_question:
    # Phase 2 : Méthode proposée
    st.header("2. Méthode proposée par Oratis")

    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    prompt_method = f"""
    Tu es un formateur Marcopolo. Ta mission est d'analyser une problématique d'utilisateur et de recommander 
    une méthode d'accompagnement adaptée (ex: DESC, OPA, SMART, QQOQCCP...).

    Problématique : {user_question}

    Donne une explication claire, pédagogique et structurée de la méthode choisie.
    """

    response_method = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt_method}],
        temperature=0.7,
        max_tokens=700,
    )

    method_explanation = response_method.choices[0].message.content
    st.success(method_explanation)
    jouer_voix_elevenlabs(method_explanation)

    # Phase 3 : Exemple illustré
    st.header("3. Exemple illustré")

    prompt_example = f"""
    En te basant sur la méthode proposée précédemment, écris un exemple concret de ce que dirait un manager dans ce cas :
    "{user_question}"

    Sois clair, bienveillant, crédible et proche de la réalité terrain.
    """

    response_example = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt_example}],
        temperature=0.7,
        max_tokens=300,
    )

    example_text = response_example.choices[0].message.content
    st.info(example_text)

    # Phase 4 : Mise en situation
    st.header("4. Mise en situation")
    user_reply = st.text_area("Imagine que tu parles à ton collaborateur. Que lui dirais-tu ?", height=150)

    # Phase 5 : Feedback IA
    if user_reply:
        st.header("5. Feedback Oratis")

        prompt_feedback = f"""
        Tu es un formateur Marcopolo. Tu vas évaluer ce message en lien avec la méthode proposée précédemment.
        Message de l'utilisateur :
        {user_reply}

        Donne un retour structuré et bienveillant à l'utilisateur. Dis-lui ce qui fonctionne, 
        ce qui pourrait être amélioré, et propose des formulations plus efficaces si besoin.
        """

        response_feedback = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt_feedback}],
            temperature=0.7,
            max_tokens=500,
        )

        feedback = response_feedback.choices[0].message.content
        st.success(feedback)
        jouer_voix_elevenlabs(feedback)
