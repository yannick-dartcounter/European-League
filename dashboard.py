import streamlit as st
import pandas as pd
import json

st.title("🎯 DartCounter Game Dashboard")

# Laad lokaal JSON-bestand
with open("game_data.json") as f:
    game_data = json.load(f)

# Bouw tabel
rows = []
for game in game_data:
    try:
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
    except:
        continue

df = pd.DataFrame(rows)
st.dataframe(df.sort_values("Score", ascending=False))
