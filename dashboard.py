import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- CONFIG ---
TOERNOOI_URL = "https://dartcounter.app/tournaments/european-league-day-2-2piSdd"

st.title("🎯 DartCounter Toernooi Dashboard")
st.caption(f"Data van: {TOERNOOI_URL}")

# --- Scraper functie ---
@st.cache_data
def scrape_tournament_stats(url):
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Kon pagina niet ophalen: {response.status_code}")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Zoek de juiste tabel (op basis van header tekst)
    tables = soup.find_all("table")
    df = None

    for table in tables:
        headers = [th.text.strip() for th in table.find_all("th")]
        if "Player" in headers and "180s" in headers:
            rows = []
            for row in table.find_all("tr")[1:]:
                cells = [td.text.strip() for td in row.find_all("td")]
                if cells:
                    rows.append(cells)
            df = pd.DataFrame(rows, columns=headers)
            break

    return df

# --- Ophalen & tonen ---
data = scrape_tournament_stats(TOERNOOI_URL)

if data.empty:
    st.warning("Geen data gevonden. Controleer de URL of wacht even.")
else:
    # Eventueel converteren naar juiste types
    numeric_cols = ["180s", "High Finish", "Legs For", "Legs Against"]
    for col in numeric_cols:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    
    # Legsaldo berekenen
    if "Legs For" in data.columns and "Legs Against" in data.columns:
        data["Legsaldo"] = data["Legs For"] - data["Legs Against"]

    st.subheader("📊 Spelerstatistieken")
    st.dataframe(data.sort_values("Legsaldo", ascending=False))

    # Grafieken
    if "180s" in data.columns:
        st.subheader("🎯 Aantal 180'ers per speler")
        st.bar_chart(data.set_index("Player")["180s"])

    if "Legsaldo" in data.columns:
        st.subheader("➕ Legsaldo per speler")
        st.bar_chart(data.set_index("Player")["Legsaldo"])
