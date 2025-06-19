import streamlit as st
from openai import OpenAI

st.image("Marcopolo_logo_def.png", width=200)
st.title("Oratis – Coach IA Marcopolo")
st.markdown("Bienvenue dans Oratis, ton formateur IA qui t’aide à bien dire.")

# Récupération sécurisée de la clé API (via secrets Streamlit Cloud)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Phase 1 : Question utilisateur
st.header("1. Pose ta question")
user_question = st.text_input("Quel est ton besoin ? (ex: Comment recadrer un collaborateur ?)")

if user_question:
    # Phase 2 : Analyse de la méthode adaptée
    st.header("2. Méthode proposée par Oratis")
    with st.spinner("Oratis réfléchit à la méthode la plus adaptée..."):
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": (
                    "Tu es un formateur Marcopolo. En fonction du besoin exprimé par l'utilisateur, "
                    "tu choisis la méthode la plus adaptée parmi : DESC (recadrage), SMART (objectifs), "
                    "OPA (questionnement), CAB (argumentaire), QQOQCP (analyse), SONCAS (décision), "
                    "BBR (objections), Écoute active, Feedback positif, Reformulation. "
                    "Explique ton choix avec pédagogie.")},
                {"role": "user", "content": user_question}
            ],
            temperature=0.7,
            max_tokens=400
        )
        method_response = response.choices[0].message.content.strip()
    st.success(method_response)

    # Phase 3 : Exemple illustré (placeholder)
    st.header("3. Exemple illustré")
    st.info("Exemple : 'Claire, j’ai remarqué que tu rends souvent les dossiers en retard (Décrire)...'")

    # Phase 4 : Simulation utilisateur
    st.header("4. Mise en situation")
    user_reply = st.text_area("Imagine que tu t’adresses à ton interlocuteur. Que lui dirais-tu ?", height=150)

    # Phase 5 : Feedback IA personnalisé avec GPT-4 Turbo
import openai

if user_reply:
    st.header("5. Feedback Oratis")

    prompt = f"""
   Tu es un formateur Marcopolo. Tu vas évaluer un message selon la méthode {detected_method}.

    Message de l'utilisateur :
    """{user_reply}"""
    Donne un retour structuré et bienveillant à l'utilisateur. Dis-lui s'il suit bien les étapes de la méthode {detected_method}, 
    ce qui est clair, ce qu’il pourrait améliorer, et comment il pourrait formuler autrement si besoin.
    """

    Ton retour doit :
    - Dire si les 4 parties sont présentes
    - Donner un conseil de formulation s’il manque quelque chose
    - Être bienveillant, structurant, formateur
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
    )

    feedback = response.choices[0].message.content
    st.success(feedback)
