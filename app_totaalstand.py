import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="European League Totaalstand", layout="wide")
st.title("🏆 Totaalstand – European League")

# 📁 URL naar Excelbestand op GitHub
url = "https://raw.githubusercontent.com/yannick-dartcounter/European-League/main/totaalstand_EL1_EL8.xlsx"

@st.cache_data(ttl=60)
def laad_excel_van_github(url):
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_excel(BytesIO(response.content))
    last_updated = response.headers.get("Last-Modified", "")
    if last_updated:
        last_updated = datetime.strptime(last_updated, "%a, %d %b %Y %H:%M:%S %Z")
    else:
        last_updated = datetime.now()
    return df, last_updated

# 📥 Data ophalen
try:
    df, last_updated = laad_excel_van_github(url)
    if df.empty or df.shape[1] == 0:
        st.cache_data.clear()
        st.experimental_rerun()
except Exception as e:
    st.error("❌ Fout bij het laden van de totaaltabel:")
    st.exception(e)
    st.stop()

# ✅ Alleen gewenste kolommen selecteren
kolommen_bewaren = [
    "Rang", "Speler", "Score", "180'ers", "100+ finishes", "Totaal", "Winnaar", "3-Darts Gemiddelde"
]
df = df[kolommen_bewaren]

# 🔁 Kolomnamen aanpassen voor weergave
df.rename(columns={
    "Rang": "Pos",
    "Speler": "Player",
    "Score": "Match Pts",
    "180'ers": "180s",
    "100+ finishes": "100+",
    "3-Darts Gemiddelde": "3-Dart Avg",
    "Totaal": "Total",
    "Winnaar": "Winner"
}, inplace=True)

# 🏆 Winnaar-icoon toevoegen
df["Winner"] = df["Winner"].apply(lambda x: "🏆" if x == 1 else "")

# 📊 Tabel tonen
df.set_index("Pos", inplace=True)
st.caption(f"📅 Laatste update: {last_updated.strftime('%d-%m-%Y %H:%M:%S')} UTC")
st.dataframe(df.style.format({
    "3-Dart Avg": "{:.2f}"
}))
