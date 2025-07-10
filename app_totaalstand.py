import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime

# Pagina volledig breed tonen
st.set_page_config(page_title="European League Ranking", layout="wide")

# Titel
st.title("🏆 Total Ranking European League")

# Raw GitHub-link naar Excelbestand
url = "https://raw.githubusercontent.com/yannick-dartcounter/European-League/main/totaalstand_EL1_EL8.xlsx"

# Data laden van GitHub
@st.cache_data(ttl=1)
def laad_excel_van_github(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_excel(BytesIO(response.content))

        # Haal laatste wijzigingsdatum uit headers
        last_modified = response.headers.get("Last-Modified")
        last_updated = None
        if last_modified:
            last_updated = datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S %Z")

        return df, last_updated
    except Exception as e:
        st.error(f"❌ Fout bij laden Excelbestand:\n\n{e}")
        return None, None

# Laad de Excel-data
df, last_updated = laad_excel_van_github(url)

if df is not None:
    # Laatst bijgewerkt datum tonen
    if last_updated:
        st.caption(f"📅 Laatst bijgewerkt: {last_updated.strftime('%d-%m-%Y %H:%M:%S')} UTC")

    # Tabel tonen met automatische kolombreedte
    st.table(df)

    # Download-knop
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "ranking_european_league.csv", "text/csv")
else:
    st.warning("⚠️ Kon totaalstand niet laden van GitHub.")
