import streamlit as st
import pandas as pd

df_players = pd.read_csv("../data/players.csv")
df_agents = df_players[df_players["is_human"] == False]

st.title("Voir le descriptif des agents")
st.write(
    "Les agents sont des entités contrôlées par l'ordinateur qui interagissent avec les jeux selon des stratégies définies."
)

st.dataframe(df_agents)
# afficher name, descriptif, strategy, et games_played
# afficher avec qui il prefere jouer -> peut etre un graphe ?
