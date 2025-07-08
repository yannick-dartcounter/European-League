import streamlit as st
import pandas as pd
import requests

# Basisconfiguratie
TOURNAMENT_ID = "2piSdd"
API_BASE = "https://dartcounter.app"
TOURNAMENT_API = f"{API_BASE}/api/tournaments/{TOURNAMENT_ID}"
MATCHES_API = f"{API_BASE}/api/tournaments/{TOURNAMENT_ID}/matches"
STATS_API = f"{API_BASE}/api/tournaments/{TOURNAMENT_ID}/stats"

# Zet titel van de app
st.title("DartCounter Toernooi Dashboard")

# Ophalen van gegevens uit de DartCounter API
try:
    tournament = requests.get(TOURNAMENT_API).json()
    matches = requests.get(MATCHES_API).json()
    stats = requests.get(STATS_API).json()
except Exception as e:
    st.error(f"Kon data niet ophalen: {e}")
    st.stop()

st.subheader(f"Toernooi: {tournament['name']}")
st.write(f"Aantal wedstrijden: {len(matches)}")

# Verwerken van spelerstatistieken
players_data = []
for sp in stats["players"]:
    players_data.append({
        "Naam": sp["name"],
        "Gespeelde wedstrijden": sp.get("matchesPlayed", 0),
        "Gewonnen": sp.get("matchesWon", 0),
        "Legs voor": sp.get("legsFor", 0),
        "Legs tegen": sp.get("legsAgainst", 0),
        "Saldo": sp.get("legsFor", 0) - sp.get("legsAgainst", 0),
        "180'ers": sp.get("count180", 0),
        "High Finish": sp.get("highFinish", 0),
    })

# Zet in een DataFrame
players_df = pd.DataFrame(players_data)

# Tabel tonen
st.subheader("Statistieken per speler")
st.dataframe(players_df.sort_values(by="Saldo", ascending=False))

# Grafiek: 180'ers
st.subheader("Aantal 180'ers per speler")
st.bar_chart(players_df.set_index("Naam")["180'ers"])

# Grafiek: Legs saldo
st.subheader("Legsaldo per speler")
st.bar_chart(players_df.set_index("Naam")["Saldo"])
