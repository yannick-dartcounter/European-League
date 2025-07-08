import streamlit as st
import pandas as pd
import json

st.title("🎯 DartCounter Game Dashboard")

# 📥 Laad lokaal JSON-bestand
try:
    with open("game_data.json") as f:
        game_data = json.load(f)
except Exception as e:
    st.error(f"Kon game_data.json niet laden: {e}")
    st.stop()

# 👉 Bouw DataFrame met veilige parsing
rows = []
for game in game_data:
    try:
        p1 = game['players'][0]['name']
        p2 = game['players'][1]['name']
        avg1 = game['players'][0].get('average', 0)
        avg2 = game['players'][1].get('average', 0)
        score = game.get('score') or f"{game['players'][0].get('legs', 0)} - {game['players'][1].get('legs', 0)}"

        rows.append({
            "Speler 1": p1,
            "Gemiddelde 1": avg1,
            "Speler 2": p2,
            "Gemiddelde 2": avg2,
            "Score": score
        })
    except Exception as e:
        st.warning(f"⚠️ Game overgeslagen vanwege fout: {e}")
        continue

df = pd.DataFrame(rows)

# 🔍 Debug: toon kolomnamen
st.write("📋 Kolommen:", df.columns.tolist())

# 📊 Tabel tonen met veilige sortering
if "Score" in df.columns and df["Score"].notna().all():
    st.dataframe(df.sort_values("Score", ascending=False))
else:
    st.dataframe(df.sort_values("Gemiddelde 1", ascending=False))
