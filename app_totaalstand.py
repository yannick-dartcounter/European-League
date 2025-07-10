import streamlit as st
import pandas as pd
import requests
from io import BytesIO

st.set_page_config(page_title="European League Ranking", layout="wide")
st.title("🏆 Totale Ranking European League")

# URL naar Excelbestand in GitHub
url = "https://raw.githubusercontent.com/yannick-dartcounter/European-League/main/totaalstand_EL1_EL8.xlsx"

@st.cache_data(ttl=300)
def laad_excel_van_github(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return pd.read_excel(BytesIO(response.content))
    except:
        return None

# Laad data
df = laad_excel_van_github(url)

if df is None:
    st.error("❌ Kon het Excelbestand niet laden van GitHub.")
else:
    # Sorteer en voeg ranking toe
    df = df.sort_values(by=["Totaal", "Score", "180'ers"], ascending=False).reset_index(drop=True)
    df["Rang"] = df["Totaal"].rank(method="min", ascending=False).astype(int)
    df = df[["Rang", "Speler", "Score", "180'ers", "100+ finishes", "Totaal"]]

    # Sidebar filter
    st.sidebar.header("🔍 Filter")
    min_score = st.sidebar.slider("Minimale totaalscore", 0, int(df['Totaal'].max()), 0)
    df_filtered = df[df["Totaal"] >= min_score]

    st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)

    # Download-knop
    csv = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "ranking.csv", "text/csv")
