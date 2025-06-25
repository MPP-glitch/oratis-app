import streamlit as st
import openai
import requests

# Titre
st.title("Oratis – Coach IA Marcopolo")
st.write("Bienvenue dans Oratis, ton formateur IA qui t’aide à bien dire.")

# Initialisation des variables de session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "oratis_starts" not in st.session_state:
    st.session_state.oratis_starts = False

# Fonction voix ElevenLabs
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

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        st.audio(response.content, format="audio/mp3")
    else:
        st.error("La voix d'Oratis n'a pas pu être générée.")

# Phase 1 : Demande
st.header("1. Pose ta question")
user_question = st.text_input("Quel est ton besoin ? (ex: Comment recadrer un collaborateur ?)")

if user_question:
    # Phase 2 : Méthode
    st.header("2. Méthode proposée par Oratis")

    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    prompt_method = f"""
    Tu es un formateur Marcopolo. Ta mission est d'analyser une problématique d'utilisateur et de recommander 
    une méthode d'accompagnement adaptée (ex: DESC, OPA, SMART, etc.).

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
        max_tokens=500,
    )
    example_text = response_example.choices[0].message.content
    st.info(example_text)
    jouer_voix_elevenlabs(example_text)

    # Phase 4 : Simulation avec Oratis
    st.header("4. Simulation avec Oratis")
    starter = st.radio("Qui commence la conversation ?", ["Moi", "Oratis"])

    if st.button("Lancer la simulation"):
        st.session_state.oratis_starts = starter == "Oratis"
        st.session_state.messages = []

    if st.session_state.oratis_starts and not st.session_state.messages:
        ouverture = f"""
        Tu es un collaborateur professionnel qui joue un rôle dans une simulation.
        L'utilisateur souhaite s'entraîner à s'exprimer selon la méthode vue précédemment.

        Commence la conversation comme un collaborateur qui pourrait être concerné par la situation.
        """
        r = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": ouverture}],
            temperature=0.7,
            max_tokens=300,
        )
        intro = r.choices[0].message.content
        st.session_state.messages.append(("Oratis", intro))

    user_msg = st.text_input("Votre message :", key="simulation_input")
    if st.button("Envoyer"):
        if user_msg:
            st.session_state.messages.append(("Moi", user_msg))
            context = "\n".join(f"{role} : {msg}" for role, msg in st.session_state.messages)
            prompt_simulation = f"""
            Tu es un collaborateur qui réponds dans un jeu de rôle. Sois réaliste, humain, bienveillant mais un peu résistant si nécessaire.

            Conversation en cours :
            {context}
            """
            r = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt_simulation}],
                temperature=0.7,
                max_tokens=300,
            )
            reply = r.choices[0].message.content
            st.session_state.messages.append(("Oratis", reply))

    for role, msg in st.session_state.messages:
        if role == "Moi":
            st.markdown(f"**Moi :** {msg}")
        else:
            st.markdown(f"**Oratis :** {msg}")
            jouer_voix_elevenlabs(msg)

    # Phase 5 : Feedback
    st.header("5. Feedback Oratis")
    if st.session_state.messages:
        last_user_inputs = "\n".join(f"{r}: {m}" for r, m in st.session_stat_
