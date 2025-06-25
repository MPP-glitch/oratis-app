import streamlit as st
import openai
import requests

st.set_page_config(page_title="Oratis – Coach IA Marcopolo")

# Initialisation des états de session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "oratis_starts" not in st.session_state:
    st.session_state.oratis_starts = False

# Fonctions

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

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Titre
st.title("Oratis – Coach IA Marcopolo")
st.write("Bienvenue dans Oratis, ton formateur IA qui t’aide à bien dire.")

# PHASE 1 : Demande utilisateur
st.header("1. Pose ta question")
user_question = st.text_input("Quel est ton besoin ? (ex: Comment recadrer un collaborateur ?)")

# PHASE 2 : Méthode proposée
if user_question:
    st.header("2. Méthode proposée par Oratis")
    prompt_method = f"""
    Tu es un formateur Marcopolo. Ta mission est d'analyser une problématique d'utilisateur et de recommander 
    une méthode d'accompagnement adaptée (ex: DESC, OPA, SMART...).

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

    # PHASE 3 : Exemple illustré
    st.header("3. Exemple illustré")
    prompt_example = f"""
    En te basant sur la méthode précédemment expliquée, écris un exemple de message qu'un manager pourrait dire dans ce cas :
    {user_question}
    """
    response_example = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt_example}],
        temperature=0.7,
        max_tokens=500,
    )
    example_text = response_example.choices[0].message.content
    st.info(example_text)
    try:
        jouer_voix_elevenlabs(example_text)
    except:
        st.error("La voix d'Oratis n'a pas pu être générée.")

    # PHASE 4 : Simulation
    st.header("4. Simulation avec Oratis")
    start_choice = st.radio("Qui commence la conversation ?", ["Moi", "Oratis"])
    if st.button("Lancer la simulation"):
        st.session_state.messages = []
        st.session_state.oratis_starts = start_choice == "Oratis"
        if st.session_state.oratis_starts:
            init_prompt = f"Tu es un collaborateur simulé. Réponds de façon naturelle, professionnelle et constructive. Contexte : {user_question}"
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": init_prompt}],
                temperature=0.7,
                max_tokens=300,
            )
            oratis_first = response.choices[0].message.content
            st.session_state.messages.append(("Oratis", oratis_first))

    # Affichage de la conversation
    for r, m in st.session_state.messages:
        if r == "Moi":
            st.markdown(f"**Moi** : {m}")
        else:
            st.markdown(f"**Oratis** : {m}")

    # Champ de réponse
    with st.form("new_message_form"):
        user_new_message = st.text_area("Votre message :", key="new_message")
        submit_new = st.form_submit_button("Envoyer")

    if submit_new and user_new_message:
        st.session_state.messages.append(("Moi", user_new_message))
        history = "\n".join(f"{r}: {m}" for r, m in st.session_state.messages)
        prompt_continu = f"Voici la discussion en cours :\n{history}\n
Tu es un collaborateur simulé. Réponds avec empathie et professionnalisme."
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt_continu}],
            temperature=0.7,
            max_tokens=300,
        )
        oratis_reply = response.choices[0].message.content
        st.session_state.messages.append(("Oratis", oratis_reply))

    # PHASE 5 : Feedback sur la communication
    st.header("5. Feedback Oratis")
    if st.button("Obtenir un feedback d'Oratis sur ma communication"):
        last_user_inputs = "\n".join(f"{r}: {m}" for r, m in st.session_state.messages if r == "Moi")
        prompt_feedback = f"""
        Tu es un formateur Marcopolo. Tu vas évaluer la qualité de la communication de l'utilisateur 
        dans cette discussion selon la méthode choisie plus haut. 

        Voici ses messages :
        {last_user_inputs}

        Donne un retour structuré et bienveillant. Décris ce qui fonctionne, ce qui peut être amélioré, 
        et propose une reformulation possible.
        """
        feedback = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt_feedback}],
            temperature=0.7,
            max_tokens=500,
        )
        final_feedback = feedback.choices[0].message.content
        st.success(final_feedback)
        try:
            jouer_voix_elevenlabs(final_feedback)
        except:
            st.error("La voix d'Oratis n'a pas pu être générée.")
