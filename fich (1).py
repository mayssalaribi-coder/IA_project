import streamlit as st
import json
import requests
import traceback

# ===================== CONFIGURATION API =====================
# 🔒 Clé API intégrée directement dans le code (ne pas partager publiquement)
API_KEY = "AIzaSyCi4hp7QaEnaksgmuHBMGqY_hEjwn8UVSk"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

# ===================== FONCTION D'APPEL API =====================
def generate_text_with_api(prompt):
    """Envoie une requête à l'API Gemini et renvoie une réponse concise."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt + "\n\nRéponds de manière concise et uniquement au besoin demandé, sans explication inutile."}]}]
    }

    if not API_KEY:
        st.error("❌ Clé d'API manquante. Veuillez la définir dans le code.")
        return None

    try:
        full_api_url = f"{API_URL}?key={API_KEY}"
        response = requests.post(full_api_url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if result and result.get("candidates") and result["candidates"][0].get("content"):
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            st.error("L'API n'a pas renvoyé de texte.")
            st.json(result)
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API : {e}")
        st.warning("Vérifiez votre connexion Internet.")
        return None
    except Exception as e:
        st.error(f"Erreur inattendue : {e}")
        st.error(traceback.format_exc())
        return None

# ===================== DÉTECTION AUTOMATIQUE DE LANGAGE =====================
def detect_language(code_snippet):
    prompt = f"Détecte le langage de ce code et renvoie uniquement son nom :\n\n{code_snippet}"
    detected = generate_text_with_api(prompt)
    return detected.strip() if detected else None

# ===================== SUGGESTION D'OPTIMISATION =====================
def suggest_optimization(code_snippet, language):
    prompt = f"Donne des suggestions brèves pour améliorer ce code {language} :\n\n{code_snippet}"
    return generate_text_with_api(prompt)

# ===================== EXPLICATION DU CODE =====================
def explain_code(code_snippet):
    prompt = f"Explique ce code en quelques phrases simples et précises en français :\n\n{code_snippet}"
    return generate_text_with_api(prompt)

# ===================== VÉRIFICATION DE SYNTAXE ET GESTION D'ERREURS =====================
def check_syntax_and_errors(code_snippet, language):
    prompt = (
        f"Analyse ce code {language} et indique brièvement les erreurs de syntaxe ou exceptions possibles. "
        f"Propose seulement les corrections nécessaires.\n\n{code_snippet}"
    )
    return generate_text_with_api(prompt)

# ===================== INTERFACE UTILISATEUR STREAMLIT =====================
def main():
    st.set_page_config(page_title="Convertisseur de code IA", page_icon="💻", layout="wide")

    st.title("💡 Convertisseur & Assistant de Code ")
    st.markdown("Transformez, expliquez et corrigez votre code.")

    languages = ["Python", "JavaScript", "C++", "C", "Java", "Go", "Ruby", "PHP", "Rust", "Swift", "Kotlin"]

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Langage source :", languages, index=0)
    with col2:
        target_lang = st.selectbox("Langage cible :", languages, index=1)

    source_code = st.text_area("Collez votre code ici :", height=300, placeholder="Collez votre code ici...")

    col_convert, col_explain, col_optimize, col_check = st.columns(4)

    with col_convert:
        convert_button = st.button("🔄 Convertir")
    with col_explain:
        explain_button = st.button("🧠 Expliquer")
    with col_optimize:
        optimize_button = st.button("⚙️ Optimiser")
    with col_check:
        check_button = st.button("🪶 Vérifier syntaxe et erreurs")

    if convert_button:
        if not source_code:
            st.warning("Veuillez coller du code à convertir.")
        elif source_lang == target_lang:
            st.warning("Langages source et cible identiques.")
        else:
            with st.spinner("Conversion concise en cours..."):
                prompt = f"Convertis ce code {source_lang} en {target_lang} et ne renvoie que le code traduit, sans explication :\n\n{source_code}"
                output = generate_text_with_api(prompt)
                if output:
                    st.subheader(f"💻 Code converti en {target_lang} :")
                    st.code(output, language=target_lang.lower())

    if explain_button and source_code:
        with st.spinner("Génération d'une explication concise..."):
            explanation = explain_code(source_code)
            if explanation:
                st.subheader("🧩 Explication du code :")
                st.markdown(explanation)

    if optimize_button and source_code:
        with st.spinner("Analyse rapide et suggestions..."):
            optimization = suggest_optimization(source_code, source_lang)
            if optimization:
                st.subheader("⚙️ Suggestions d'optimisation :")
                st.markdown(optimization)

    if check_button and source_code:
        with st.spinner("Vérification concise de la syntaxe..."):
            review = check_syntax_and_errors(source_code, source_lang)
            if review:
                st.subheader("🪶 Résumé des erreurs et corrections :")
                st.markdown(review)

    st.markdown("---")
    st.caption("Cette plateforme est réalisée par Farah Ghazouani, Arij Ben Rabiaa et Mayssa Laribi")

if __name__ == "__main__":
    main()

