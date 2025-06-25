import streamlit as st
import openai
import requests

st.set_page_config(page_title="Oratis – Coach IA", layout="centered")

st.title("Oratis – Coach IA Marcopolo")
st.write("Bienvenue dans Oratis, ton formateur IA qui t’aide à bien dire.")

# ------------------ Fonction de synthèse vocale ------------------
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
        st.audio(response.content, format="audio/mp3")
    else:
        st.error("La voix d'Oratis n'a pas pu être générée.")

# ------------------ Clé API OpenAI ------------------
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------ Phase 1 : question utilisateur ------------------
st.header("1. Pose ta question")
user_question = st.text_input("Quel est ton besoin ? (ex: Comment recadrer un collaborateur ?)")

if user_question:
    # ------------------ Phase 2 : Méthode proposée ------------------
    st.header("2. Méthode proposée par Oratis")

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

    # ------------------ Phase 3 : Exemple illustré ------------------
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

    # ------------------ Phase 4 : Simulation interactive ------------------
    st.header("4. Simulation avec Oratis")

    if "messages_simulation" not in st.session_state:
        st.session_state.messages_simulation = [
            {"role": "system", "content": "Tu es Oratis, un formateur IA bienveillant. Tu aides à appliquer la méthode précédente en dialoguant avec l'utilisateur."}
        ]

    choix_init = st.radio("Qui commence la conversation ?", ["Moi", "Oratis"])

    if st.button("Lancer la simulation"):
        if choix_init == "Oratis":
            init_prompt = f"En lien avec la problématique : {user_question}, commence une conversation avec l'utilisateur pour l'aider à appliquer la méthode vue précédemment."
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=st.session_state.messages_simulation + [{"role": "user", "content": init_prompt}],
                temperature=0.7,
                max_tokens=300,
            )
            bot_reply = response.choices[0].message.content
            st.session_state.messages_simulation.append({"role": "assistant", "content": bot_reply})

    # Affichage du fil de conversation
    for msg in st.session_state.messages_simulation[1:]:
        if msg["role"] == "assistant":
            st.markdown(f"**Oratis :** {msg['content']}")
        elif msg["role"] == "user":
            st.markdown(f"**Moi :** {msg['content']}")

    user_input = st.text_input("Votre message :", key="user_msg_input")
    if st.button("Envoyer") and user_input:
        st.session_state.messages_simulation.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=st.session_state.messages_simulation,
            temperature=0.7,
            max_tokens=300,
        )
        bot_reply = response.choices[0].message.content
        st.session_state.messages_simulation.append({"role": "assistant", "content": bot_reply})

        st.rerun()

    # ------------------ Phase 5 : Feedback ------------------
    if len(st.session_state.messages_simulation) > 3:
        st.header("5. Feedback Oratis")
        full_message = "\n".join(
            [m["content"] for m in st.session_state.messages_simulation if m["role"] == "user"]
        )

        prompt_feedback = f"""
        Tu es un formateur Marcopolo. Voici un exemple de communication que l'utilisateur a tenté. 
        Évalue cette tentative selon la méthode suggérée précédemment.
        
        Texte :
        {full_message}

        Donne un retour structuré et bienveillant. Dis ce qui fonctionne, ce qui peut être amélioré, et propose des alternatives.
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
