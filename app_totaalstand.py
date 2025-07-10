import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Pagina-instellingen
st.set_page_config(page_title="European League Ranking", layout="wide")

# Titel van de app
st.title("🏆 Total Ranking European League")
st.markdown("Live overzicht van de totaalscores uit EL1 t/m EL8. De ranking wordt elke 5 minuten automatisch bijgewerkt vanuit GitHub.")

# ✅ URL naar je Excelbestand op GitHub
url = "https://raw.githubusercontent.com/yannick-dartcounter/European-League/main/totaalstand_EL1_EL8.xlsx"

# ✅ Functie om bestand in te laden
@st.cache_data(ttl=300)  # Herlaad elke 5 minuten
def laad_excel_van_github(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pd.read_excel(BytesIO(response.content))
    except Exception as e:
        st.error(f"❌ Fout bij laden Excelbestand:\n\n{e}")
        return None

# ✅ Laad de data
df = laad_excel_van_github(url)

# ✅ Verwerk en toon de data
if df is not None:
    # Sorteer en voeg ranking toe
    df = df.sort_values(by=["Totaal", "Score", "180'ers"], ascending=False).reset_index(drop=True)
    df["Rang"] = df["Totaal"].rank(method="min", ascending=False).astype(int)

    # Kolommen in juiste volgorde
    df = df[["Rang", "Speler", "Score", "180'ers", "100+ finishes", "Totaal"]]

    # Sidebar: filter op minimale totaalscore
    st.sidebar.header("🔍 Filter")
    min_score = st.sidebar.slider("Minimale totaalscore", 0, int(df["Totaal"].max()), 0)
    df_filtered = df[df["Totaal"] >= min_score]

    # Tabel tonen
    st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)

    # Download-knop
    csv = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "ranking_european_league.csv", "text/csv")
