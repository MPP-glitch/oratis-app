
import streamlit as st
import openai

st.title(" Oratis – Coach IA Marcopolo")

# Phase 1: Demande de l'utilisateur
st.header("1. Pose ta question")
user_question = st.text_input("Quel est ton besoin ? (ex: Comment recadrer un collaborateur ?)")

if user_question:
    # Phase 2 : Analyse de la méthode adaptée
    st.header("2. Méthode proposée par Oratis")
    with st.spinner("Oratis réfléchit à la méthode la plus adaptée..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "Tu es un formateur Marcopolo. En fonction du besoin exprimé par l'utilisateur, "
                    "tu choisis la méthode la plus adaptée parmi : "
                    "DESC (recadrage), SMART (formulation d'objectif), OPA (questionnement), "
                    "Méthode CAB (argumentaire commercial), Méthode QQOQCP (analyse de situation), "
                    "Méthode SONCAS (identifier leviers de décision), BBR (traitement des objections), "
                    "Écoute active (empathie), Feedback positif (reconnaissance), "
                    "Techniques de reformulation (validation compréhension). "
                    "Explique ton choix clairement, avec une formulation bienveillante et professionnelle.")},
                {"role": "user", "content": user_question}
            ],
            temperature=0.7,
            max_tokens=400
        )
        method_response = response.choices[0].message.content.strip()
    st.success(method_response)

    # Phase 3 : Exemple illustré (générique ici)
    st.header("3. Exemple illustré")
    st.info("Exemple : 'Claire, j’ai remarqué que tu rends souvent les dossiers en retard (Décrire)...'")

    # Phase 4 : Simulation utilisateur
    st.header("4. Mise en situation")
    user_reply = st.text_area("Imagine que tu t’adresses à ton interlocuteur. Que lui dirais-tu ?", height=150)

    # Phase 5 : Feedback IA simulé (fixe ici, améliorable plus tard)
    if user_reply:
        st.header("5. Feedback Oratis")
        st.success("✅ Tu as bien structuré ta réponse. Tu pourrais encore renforcer l'impact en précisant les bénéfices pour ton interlocuteur ou ton équipe.")


