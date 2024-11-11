import streamlit as st
import pandas as pd

df_players = pd.read_csv("../data/players.csv")
df_humans = df_players[df_players["is_human"] == True]

st.title("Joueurs humains")
st.write("Liste des joueurs humains.")

st.dataframe(df_humans)

# afficher le nombre de parti joué par chaque joueur