import streamlit as st
import openai
import requests

st.title("Oratis – Coach IA Marcopolo")
st.write("Bienvenue dans Oratis, ton formateur IA qui t’aide à bien dire.")

# Fonction synthèse vocale ElevenLabs
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

# Phase 1 : Question utilisateur
st.header("1. Pose ta question")
user_question = st.text_input("Quel est ton besoin ? (ex: Comment recadrer un collaborateur ?)")

if user_question:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Phase 2 : Méthode
    st.header("2. Méthode proposée par Oratis")

    prompt_method = f"""
    Tu es un formateur Marcopolo. Ta mission est de proposer une méthode d'accompagnement adaptée 
    à la problématique : "{user_question}". 
    Choisis une méthode connue (DESC, SMART, etc.), explique-la de manière claire, pédagogique et structurée.
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
    """

    response_example = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt_example}],
        temperature=0.7,
        max_tokens=400,
    )

    example_text = response_example.choices[0].message.content
    st.info(example_text)
    jouer_voix_elevenlabs(example_text)

    # Phase 4 : Simulation
    st.header("4. Simulation avec Oratis")

    if "history" not in st.session_state:
        st.session_state.history = []
    if "oratis_starts" not in st.session_state:
        st.session_state.oratis_starts = False

    choix = st.radio("Qui commence la conversation ?", ["Moi", "Oratis"])
    if st.button("Lancer la simulation"):
        st.session_state.oratis_starts = choix == "Oratis"
        st.session_state.history = []

        if st.session_state.oratis_starts:
           prompt_start = f"""
            Tu es un collaborateur simulé dans une entreprise. Tu viens d'être contacté par ton manager 
            pour discuter d’un sujet important. Commence la conversation naturellement, de manière humaine 
            et professionnelle. Ne donne pas de conseils ou de méthode, reste dans ton rôle de collaborateur.
            
            Commence simplement par un « bonjour » et propose d’échanger ou demande comment tu peux aider.
            """

            response_oratis = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt_start}],
                temperature=0.7,
                max_tokens=300,
            )
            debut = response_oratis.choices[0].message.content
            st.session_state.history.append(("Oratis", debut))

    if st.session_state.history:
        for role, message in st.session_state.history:
            if role == "Moi":
                st.markdown(f"**Moi** : {message}")
            else:
                st.markdown(f"**Oratis** : {message}")

        user_msg = st.text_input("Votre message :")
        if st.button("Envoyer"):
            st.session_state.history.append(("Moi", user_msg))

            history = "\n".join([f"{r}: {m}" for r, m in st.session_state.history])
            prompt_continu = f"Voici la discussion en cours :\n{history}\nTu es un collaborateur simulé. Réponds avec empathie et professionnalisme."

            response_suite = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt_continu}],
                temperature=0.7,
                max_tokens=300,
            )

            oratis_reply = response_suite.choices[0].message.content
            st.session_state.history.append(("Oratis", oratis_reply))

    # Phase 5 : Feedback
    st.header("5. Feedback Oratis")

    if st.button("Demander le feedback final"):
        full_history = "\n".join([f"{r}: {m}" for r, m in st.session_state.history])
        prompt_feedback = f"""
        Voici une simulation de discussion entre un manager et un collaborateur :
        {full_history}

        Donne un feedback constructif au manager sur la qualité de sa communication :
        - Ce qui est clair et positif
        - Ce qui peut être amélioré
        - Des reformulations utiles
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
