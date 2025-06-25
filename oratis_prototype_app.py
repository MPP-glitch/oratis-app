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
    jouer_voix_elevenlabs(example_text)  # 🔊 Ajout de l'audio pour la phase 3

    # Phase 4 : Mise en situation
 # Phase 4 : Simulation libre (dialogue dynamique)
st.header("4. Simulation avec Oratis")

if "dialogue" not in st.session_state:
    st.session_state.dialogue = []

if "start_by" not in st.session_state:
    st.session_state.start_by = None

if st.session_state.start_by is None:
    start_choice = st.radio("Qui commence la conversation ?", ["Moi", "Oratis"])
    if st.button("Lancer la simulation"):
        st.session_state.start_by = start_choice
        if start_choice == "Oratis":
            opening_line = f"Bonjour, concernant votre problématique « {user_question} », pouvez-vous m'expliquer comment vous souhaitez procéder ?"
            st.session_state.dialogue.append(("Oratis", opening_line))

# Affichage du dialogue existant
for speaker, msg in st.session_state.dialogue:
    if speaker == "Oratis":
        st.markdown(f"**🧠 Oratis :** {msg}")
    else:
        st.markdown(f"**🗣️ Vous :** {msg}")

# Entrée utilisateur
if st.session_state.start_by:
    user_input = st.text_input("Votre message :", key="simulation_input")
    if st.button("Envoyer", key="send_simulation"):
        if user_input:
            st.session_state.dialogue.append(("Vous", user_input))

            # Construction du prompt avec historique
            historique = ""
            for speaker, msg in st.session_state.dialogue:
                prefix = "Collaborateur" if speaker == "Oratis" else "Utilisateur"
                historique += f"{prefix} : {msg}\n"

            prompt_oratis = f"""
Tu joues le rôle d'un collaborateur ou prospect dans une simulation pédagogique avec un apprenant.
Tu dois répondre de façon réaliste, bienveillante, et engager la conversation.
Tu adaptes ton style en fonction de cette méthode : {method_explanation[:300]}...

Voici l’historique de l’échange :
{historique}

Formule une réponse courte (1 à 3 phrases), naturelle, humaine, en cohérence avec la méthode et la problématique.
"""

            response_simulation = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt_oratis}],
                temperature=0.7,
                max_tokens=300,
            )

            oratis_reply = response_simulation.choices[0].message.content.strip()
            st.session_state.dialogue.append(("Oratis", oratis_reply))

# Phase 5 : Feedback Oratis
st.header("5. Feedback Oratis")

if st.session_state.get("dialogue"):
    # Construction de l'historique pour évaluation
    historique = ""
    for speaker, msg in st.session_state.dialogue:
        prefix = "Collaborateur" if speaker == "Oratis" else "Utilisateur"
        historique += f"{prefix} : {msg}\n"

    prompt_feedback = f"""
Tu es un formateur Marcopolo. Tu vas évaluer l’ensemble de cet échange entre un utilisateur et un collaborateur simulé.

Voici la méthode que l’utilisateur devait appliquer :
{method_explanation[:300]}...

Voici l’historique de la simulation :
{historique}

Fais un retour structuré et bienveillant à l'utilisateur. Dis-lui :
- ce qu'il a bien fait
- ce qu'il peut améliorer
- propose des formulations plus efficaces si besoin

Sois encourageant et formateur.
"""

    response_feedback = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt_feedback}],
        temperature=0.7,
        max_tokens=500,
    )

    feedback = response_feedback.choices[0].message.content.strip()
    st.success(feedback)

    # Lecture audio facultative
    jouer_voix_elevenlabs(feedback)
