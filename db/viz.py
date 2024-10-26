import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from secret.config import DATABASE_URL

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Connexion à la base de données
engine = create_engine(DATABASE_URL)

# Titre de l'application
st.title("Analyse de Données des Jeux")

# Charger les données
query = "SELECT * FROM player;"  # Exemple pour obtenir les données de la table player
df = pd.read_sql(query, engine)
st.write("Aperçu des données :", df.head())

# Exemple de graphique avec Seaborn
st.subheader("Distribution des Scores des Participants")
fig, ax = plt.subplots()
sns.histplot(df["score"], bins=10, kde=True, ax=ax)
st.pyplot(fig)

# Graphique Plotly pour des visualisations interactives
import plotly.express as px

fig = px.bar(df, x='name', y='score', title="Score par Joueur")
st.plotly_chart(fig)
