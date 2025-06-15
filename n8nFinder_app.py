
import streamlit as st
import pandas as pd

st.set_page_config(page_title="n8nFinder", layout="wide")

# Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv("workflows_catalogue_streamlit.csv")

df = load_data()
st.subheader("🧪 Aperçu du fichier CSV chargé")
st.write(df.head(10))
st.info(f"📊 Le fichier contient {len(df)} lignes.")

st.title("🔍 n8nFinder – Catalogue intelligent de workflows")
st.markdown("Trouvez rapidement le workflow n8n adapté à vos besoins : plateforme, usage, score...")

# Filtres
col1, col2, col3 = st.columns(3)

with col1:
    plateforme = st.selectbox("🧩 Plateforme", ["Toutes"] + sorted(df["Plateforme"].dropna().unique().tolist()))
with col2:
    categorie = st.selectbox("📂 Catégorie", ["Toutes"] + sorted(df["Catégorie"].dropna().unique().tolist()))
with col3:
    pret = st.selectbox("✅ Prêt à l’emploi ?", ["Tous", "Oui", "Non"])

# Filtrage
filtered_df = df.copy()
if plateforme != "Toutes":
    filtered_df = filtered_df[filtered_df["Plateforme"] == plateforme]
if categorie != "Toutes":
    filtered_df = filtered_df[filtered_df["Catégorie"] == categorie]
if pret != "Tous":
    filtered_df = filtered_df[filtered_df["Prêt à l’emploi ?"] == pret]

# Recherche plein texte
search = st.text_input("🔎 Recherche (nom, Résumé auto, tags)").strip().lower()
if search:
    filtered_df = filtered_df[
        filtered_df["Nom du workflow"].str.lower().str.contains(search) |
        filtered_df["Résumé auto"].str.lower().str.contains(search) |
        filtered_df["Tags"].str.lower().str.contains(search)
    ]

# Affichage
st.markdown(f"### Résultats : {len(filtered_df)} workflow(s) trouvé(s)")

for _, row in filtered_df.iterrows():
    st.markdown(f"""
    ---
    ### 📌 {row["Nom du workflow"]}
    **Résumé auto :** {row["Résumé auto"]}  
    **Plateforme :** {row["Plateforme"]} | **Catégorie :** {row["Catégorie"]} | **Domaine :** {row["Domaine"]}  
    **Tags :** {row.get("Tags", "—")}` | **Score :** {row["Score"]}  
    🗂️ Fichier : `{row["Fichier"]}` | Prêt à l’emploi : **{row["Prêt à l’emploi ?"]}**
    """)
