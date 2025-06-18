
import streamlit as st
import openai

st.title("🧠 Oratis – Coach IA Marcopolo")

# Phase 1: Demande de l'utilisateur
st.header("1. Pose ta question")
user_question = st.text_input("Quel est ton besoin ? (ex: Comment recadrer un collaborateur ?)")

if user_question:
    # Phase 2: Explication de la méthode
    st.header("2. Méthode proposée par Oratis")
    st.markdown("✍️ Oratis explique une méthode adaptée à ta problématique...")

    # Simulated response
    method_response = f"Pour répondre à ta demande ({user_question}), Oratis recommande d'utiliser la méthode DESC : Décrire, Exprimer, Suggérer, Conclure."
    st.success(method_response)

    # Phase 3: Exemple concret
    st.header("3. Exemple illustré")
    example = f"Exemple : 'Claire, j’ai remarqué que tu rends souvent les dossiers en retard (Décrire)... Je me sens en difficulté pour tenir les délais (Exprimer)... Je te propose qu’on se mette d’accord ensemble sur un planning plus clair (Suggérer)... D’accord ? (Conclure)'"
    st.info(example)

    # Phase 4: Simulation utilisateur
    st.header("4. Mise en situation")
    user_reply = st.text_area("Imagine que tu parles à Claire. Que lui dirais-tu ?", height=150)

    if user_reply:
        # Phase 5: Feedback IA simulé
        st.header("5. Feedback Oratis")
        feedback = "✅ Tu as bien commencé avec une observation factuelle. Tu pourrais renforcer la partie 'Exprimer' en ajoutant ton ressenti personnel. Essaie d’éviter les jugements, reste factuel et empathique."
        st.success(feedback)
