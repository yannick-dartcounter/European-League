import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime

# Pagina-indeling: volledig scherm
st.set_page_config(page_title="European League Ranking", layout="wide")

# Titel en uitleg
st.title("🏆 Totale Ranking European League")

# GitHub raw link naar Excelbestand
url = "https://raw.githubusercontent.com/yannick-dartcounter/European-League/main/totaalstand_EL1_EL8.xlsx"

# Data ophalen van GitHub (Excel)
@st.cache_data(ttl=300)  # vernieuw elke 5 minuten
def laad_excel_van_github(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_excel(BytesIO(response.content))

        # Haal ook de 'Last-Modified' header op
        last_modified = response.headers.get("Last-Modified", None)
        if last_modified:
            last_updated = datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S %Z")
        else:
            last_updated = None

        return df, last_updated

    except Exception as e:
        st.error(f"❌ Fout bij laden Excelbestand:\n\n{e}")
        return None, None

# Laad data
df, last_updated = laad_excel_van_github(url)

if df is not None:
    # Sorteer en bereken ranking
    df = df.sort_values(by=["Totaal", "Score", "180'ers"], ascending=False).reset_index(drop=True)
    df["Rang"] = df["Totaal"].rank(method="min", ascending=False).astype(int)

    # Kolommen herschikken
    df = df[["Rang", "Speler", "Score", "180'ers", "100+ finishes", "Totaal"]]

    # Sidebar filter
    st.sidebar.header("🔍 Filter")
    min_score = st.sidebar.slider("Minimale totaalscore", 0, int(df["Totaal"].max()), 0)
    df_filtered = df[df["Totaal"] >= min_score]

    # Laatst bijgewerkt tonen (indien beschikbaar)
    if last_updated:
        st.caption(f"📅 Laatst bijgewerkt: {last_updated.strftime('%d-%m-%Y %H:%M:%S')} (UTC)")

    # Toon de tabel
    st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)

    # Downloadknop
    csv = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "ranking_european_league.csv", "text/csv")
else:
    st.warning("Er kon geen data worden geladen. Controleer of het Excelbestand in GitHub aanwezig is.")
