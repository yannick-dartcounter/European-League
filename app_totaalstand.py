import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime

# Volledig scherm gebruiken
st.set_page_config(page_title="European League Ranking", layout="wide")

# Titel
st.title("🏆 Total Ranking European League")

# GitHub raw link naar Excelbestand
url = "https://raw.githubusercontent.com/yannick-dartcounter/European-League/main/totaalstand_EL1_EL8.xlsx"

# Functie om Excel van GitHub te laden
@st.cache_data(ttl=1)
def laad_excel_van_github(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_excel(BytesIO(response.content))

        # Parse 'Last-Modified' header als datetime
        last_modified = response.headers.get("Last-Modified", None)
        if last_modified:
            last_updated = datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S %Z")
        else:
            last_updated = None

        return df, last_updated
    except Exception as e:
        st.error(f"❌ Fout bij laden Excelbestand:\n\n{e}")
        return None, None

# Data ophalen
df, last_updated = laad_excel_van_github(url)

if df is not None:
    # Sorteer en bereken ranking
    df = df.sort_values(by=["Totaal", "Score", "180'ers"], ascending=False).reset_index(drop=True)
    df["Rang"] = df["Totaal"].rank(method="min", ascending=False).astype(int)
    df = df[["Rang", "Speler", "Score", "180'ers", "100+ finishes", "Totaal"]]

    # Laatst bijgewerkt tonen
    if last_updated:
        st.caption(f"📅 Laatst bijgewerkt: {last_updated.strftime('%d-%m-%Y %H:%M:%S')} UTC")

    # Toon volledige ranking zonder index en met meer hoogte
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=1000
    )

    # Download-knop
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "ranking_european_league.csv", "text/csv")

else:
    st.warning("⚠️ Kon geen data laden.")
