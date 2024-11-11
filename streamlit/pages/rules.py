import streamlit as st
import pandas as pd

df_players = pd.read_csv("../data/players.csv")
df_rules = pd.read_csv("../data/is_rule.csv")

st.title("Voir le descriptif des règles")

# afficher les règles des jeux
st.dataframe(df_rules)