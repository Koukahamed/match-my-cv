import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="MatchMyCV", page_icon="🎯", layout="wide")

# --- GESTION DES SECRETS (Clé API) ---
# Sur Streamlit Cloud, tu devras ajouter GEMINI_API_KEY dans les "Secrets"
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Entre ta clé API Gemini :", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Température basse (0.3) pour plus de rigueur et moins de "blabla"
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"temperature": 0.3})

    st.title("🚀 MatchMyCV : Optimiseur Intelligent")
    st.markdown("Optimise ton CV en fonction d'une offre d'emploi spécifique grâce à l'IA.")

    # --- ZONE DE SAISIE ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Ton CV actuel")
        cv_text = st.text_area("Copie-colle le contenu de ton CV ici :", height=400, placeholder="Expériences, compétences, formations...")

    with col2:
        st.subheader("💼 L'Offre d'Emploi")
        job_text = st.text_area("Copie-colle le descriptif du poste ici :", height=400, placeholder="Missions, profil recherché, requis...")

    # --- LOGIQUE D'ANALYSE ---
    if st.button("Analyser et Optimiser ✨", use_container_width=True):
        if cv_text and job_text:
            with st.spinner('Analyse chirurgicale en cours...'):
                try:
                    prompt = f"""
                    Agis en tant qu'Expert en Recrutement et spécialiste ATS. 
                    Analyse le CV par rapport à l'offre d'emploi ci-dessous.
                    
                    CV : 
                    {cv_text}
                    
                    OFFRE D'EMPLOI : 
                    {job_text}
                    
                    Réponds EXCLUSIVEMENT avec ce format structuré :
                    
                    # 🎯 Score de Matching : [X/100]
                    
                    ## 🛠️ Analyse des Compétences
                    | Compétence Requise | Présente dans le CV | Statut |
                    | :--- | :--- | :--- |
                    | [Nom Compétence] | [Oui/Non] | [✅/❌] |
                    
                    ## 📝 Suggestions de Réécriture (Impact & Chiffres)
                    Prends une ou deux expériences du CV et réécris-les pour qu'elles collent aux besoins de l'offre en utilisant des verbes d'action.
                    
                    **Ancienne version :** "[Texte original]"
                    **Version optimisée :** "[Ta proposition]"
                    
                    ## 💡 Top 3 Conseils Stratégiques
                    1. [Conseil sur la structure ou les mots-clés]
                    2. [Conseil sur le positionnement]
                    3. [Conseil sur les manques éventuels]
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Erreur lors de l'analyse : {e}")
        else:
            st.warning("⚠️ Veuillez remplir les deux champs (CV et Annonce) avant de lancer.")
else:
    st.info("👋 Bienvenue ! Veuillez configurer votre clé API Gemini dans les paramètres ou la barre latérale pour commencer.")

# --- FOOTER ---
st.markdown("---")
st.caption("MatchMyCV - Outil d'aide à l'optimisation de candidature - Propulsé par Gemini AI")