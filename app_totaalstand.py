import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="European League Ranking", layout="wide")
st.title("🏆 Total Ranking European League")

# 📁 URL naar Excelbestand op GitHub
url = "https://raw.githubusercontent.com/yannick-dartcounter/European-League/main/totaalstand_EL1_EL8.xlsx"

@st.cache_data(ttl=600)
def laad_excel_van_github(url):
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_excel(BytesIO(response.content))
    last_updated = response.headers.get("Last-Modified", "")
    if last_updated:
        last_updated = datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S %Z")
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
    st.error("❌ Error loading Excel file:")
    st.exception(e)
    st.stop()

# 🕒 Laatste update tonen
st.caption(f"📅 Last updated: {last_updated.strftime('%d-%m-%Y %H:%M:%S')} UTC")

# 🔽 Downloadknop
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="ranking_european_league.csv",
    mime="text/csv"
)

# 🔧 Verwijder index en vertaal kolomnamen
df.reset_index(drop=True, inplace=True)
df.rename(columns={
    "Rang": "Rank",
    "Speler": "Player",
    "180'ers": "180's",
    "Totaal": "Total"
}, inplace=True)

# 📊 AgGrid weergave
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(resizable=True, wrapText=True, autoHeight=True)
gb.configure_grid_options(domLayout='autoHeight')
gb.configure_pagination(enabled=False)
grid_options = gb.build()

AgGrid(
    df,
    gridOptions=grid_options,
    theme="balham",
    height=None,
    reload_data=True,
    allow_unsafe_jscode=False
)
