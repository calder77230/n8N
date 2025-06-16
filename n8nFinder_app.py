import streamlit as st
import pandas as pd
from io import StringIO
import base64

st.set_page_config(page_title="n8nFinder Pro", layout="wide")

# 🔄 Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv("workflows_catalogue_streamlit.csv")

df = load_data()

# 🎈 Titre & Aperçu
st.title("\ud83e\udd16 n8nFinder Pro – Le catalogue IA ultime des workflows")
st.markdown("Filtrez, recherchez, explorez et téléchargez instantanément les workflows n8n les plus pertinents.")

st.dataframe(df.head(10), use_container_width=True)
st.info(f"\ud83d\udcca {len(df)} workflows chargés.")

# 🔢 Filtres
col1, col2, col3, col4 = st.columns(4)
with col1:
    plateforme = st.selectbox("\ud83c\udf31 Plateforme", ["Toutes"] + sorted(df["Plateforme"].dropna().unique().tolist()))
with col2:
    categorie = st.selectbox("\ud83d\udcbc Catégorie", ["Toutes"] + sorted(df["Catégorie"].dropna().unique().tolist()))
with col3:
    domaine = st.selectbox("\ud83d\udcc8 Domaine", ["Tous"] + sorted(df["Domaine"].dropna().unique().tolist()))
with col4:
    pret = st.selectbox("\ud83d\udcc5 Prêt à l’emploi ?", ["Tous", "Oui", "Non"])

# 🔍 Recherche plein texte
search = st.text_input("\ud83d\udd0d Recherche intelligente (titre, résumé, tags, domaine...)").strip().lower()

# 🔀 Filtrage logiques combinées
filtered_df = df.copy()
if plateforme != "Toutes":
    filtered_df = filtered_df[filtered_df["Plateforme"] == plateforme]
if categorie != "Toutes":
    filtered_df = filtered_df[filtered_df["Catégorie"] == categorie]
if domaine != "Tous":
    filtered_df = filtered_df[filtered_df["Domaine"] == domaine]
if pret != "Tous":
    filtered_df = filtered_df[filtered_df["Prêt à l’emploi ?"] == pret]
if search:
    filtered_df = filtered_df[
        filtered_df["Nom du workflow"].str.lower().str.contains(search) |
        filtered_df["Résumé auto"].str.lower().str.contains(search) |
        filtered_df.get("Tags", pd.Series("")).astype(str).str.lower().str.contains(search) |
        filtered_df["Domaine"].astype(str).str.lower().str.contains(search)
    ]

# 🌟 Tri par score
filtered_df = filtered_df.sort_values(by="Score", ascending=False)

# 📃 Export CSV dynamique
def get_csv_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="n8nFinder_resultats.csv">\ud83d\udcc2 Télécharger les résultats (.csv)</a>'
    return href

st.markdown(get_csv_download_link(filtered_df), unsafe_allow_html=True)

# 📄 Affichage enrichi
st.markdown(f"### \ud83c\udf10 {len(filtered_df)} workflows trouvés")
for _, row in filtered_df.iterrows():
    st.markdown(f"""
---
### 📍 {row.get("Nom du workflow", "Sans titre")}
**Résumé auto :** {row.get("Résumé auto", "\u2014")}
**Plateforme :** {row.get("Plateforme", "\u2014")} | **Catégorie :** {row.get("Catégorie", "\u2014")} | **Domaine :** {row.get("Domaine", "\u2014")}
**Tags :** {row.get("Tags", "\u2014")} | **Score :** {row.get("Score", "\u2014")}
📁 Fichier : `{row.get("Fichier", "Non défini")}` | Prêt à l’emploi : **{row.get("Prêt à l’emploi ?", "\u2014")}**
""")
