import streamlit as st
from google import genai
from pypdf import PdfReader
from docx import Document
import io

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="MatchMyCV AI", page_icon="🎯", layout="centered")

# --- FONCTION D'EXTRACTION DE TEXTE ---
def extract_text_from_file(uploaded_file):
    try:
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            return "".join([page.extract_text() for page in reader.pages])
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
    return None

# --- VÉRIFICATION DE LA CLÉ API ---
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ Clé API manquante. Ajoute 'GEMINI_API_KEY' dans les Secrets de Streamlit.")
    st.stop()

# Initialisation du client Gemini 3
client = genai.Client(api_key=api_key)
model_id = "gemini-3-flash" # Version rapide et efficace

# --- INTERFACE UTILISATEUR ---
st.title("🚀 MatchMyCV Pro")
st.markdown("Optimisez votre CV pour une offre spécifique en un clic.")

# Zone de téléchargement du CV
st.subheader("1. Ton CV (PDF ou Word)")
uploaded_file = st.file_uploader("Glisse ton fichier ici", type=["pdf", "docx"])

# Zone de l'annonce
st.subheader("2. L'Offre d'Emploi")
job_description = st.text_area("Copie-colle le texte de l'annonce ici :", height=250, placeholder="Missions, profil recherché...")

# Bouton d'action
if st.button("Analyser mon profil ✨", use_container_width=True):
    if uploaded_file and job_description:
        with st.spinner('Analyse en cours par Gemini 3...'):
            # Extraction du texte
            cv_text = extract_text_from_file(uploaded_file)
            
            if cv_text:
                # Construction du Prompt
                prompt = f"""
                Tu es un expert en recrutement (ATS Specialist). 
                Analyse le CV ci-dessous par rapport à l'offre d'emploi fournie.
                
                --- CV ---
                {cv_text[:8000]}
                
                --- OFFRE ---
                {job_description[:4000]}
                
                --- FORMAT DE RÉPONSE ---
                Réponds en Markdown avec :
                1. # 🎯 Score de Matching : [X/100]
                2. ## 🛠️ Analyse des Compétences (Tableau : Compétence | Présence | Impact)
                3. ## 📝 Suggestions de Réécriture (Propose 2 réécritures STAR basées sur le CV pour matcher l'offre)
                4. ## 💡 Top 3 Conseils pour ce poste spécifique
                """
                
                try:
                    # Requête à l'IA
                    response = client.models.generate_content(
                        model=model_id,
                        contents=prompt
                    )
                    
                    st.success("Analyse terminée !")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Erreur API : {e}")
            else:
                st.error("Impossible d'extraire le texte du CV.")
    else:
        st.info("Veuillez uploader un CV et coller une annonce pour lancer l'analyse.")

# --- FOOTER ---
st.markdown("---")
st.caption("MatchMyCV - Propulsé par Gemini 3 Flash - 2026")