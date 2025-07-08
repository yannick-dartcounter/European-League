import streamlit as st
import pandas as pd
import requests
import json

st.title("🎯 DartCounter Game Dashboard")

# 📥 Laad JSON vanaf GitHub
GITHUB_JSON_URL = "https://raw.githubusercontent.com/<gebruikersnaam>/<repo>/main/game_data.json"

try:
    response = requests.get(GITHUB_JSON_URL)
    game_data = response.json()
    st.success("✅ Data succesvol geladen vanaf GitHub")
except Exception as e:
    st.error(f"❌ Fout bij laden van JSON: {e}")
    st.stop()

# 👉 Bouw hierna je dashboard verder
# Bijvoorbeeld een tabel van alle games:
rows = []
for game in game_data:
    p1 = game['players'][0]['name']
    p2 = game['players'][1]['name']
    score = game.get('score', 'n.v.t.')
    avg1 = game['players'][0].get('average', 0)
    avg2 = game['players'][1].get('average', 0)
    rows.append({
        "Speler 1": p1,
        "Gemiddelde 1": avg1,
        "Speler 2": p2,
        "Gemiddelde 2": avg2,
        "Score": score
    })

df = pd.DataFrame(rows)
st.dataframe(df.sort_values("Score", ascending=False))
