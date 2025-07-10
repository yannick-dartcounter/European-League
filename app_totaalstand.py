import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime

st.set_page_config(page_title="Ranking European League", layout="wide")

@st.cache_data(ttl=600)
def laad_excel_van_github(url):
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_excel(io.BytesIO(response.content)), datetime.now()

# 📦 Excelbron
url = "https://raw.githubusercontent.com/yannick-dartcounter/European-League/main/totaalstand_EL1_EL8.xlsx"

# 🔁 Eerste poging tot laden
try:
    df, last_updated = laad_excel_van_github(url)
    # ❗ Als leeg → cache wissen en rerun
    if df.empty or df.shape[1] == 0:
        st.cache_data.clear()
        st.experimental_rerun()
except Exception as e:
    st.error("❌ Fout bij laden Excelbestand:")
    st.exception(e)
    st.stop()

# 🎯 Rest van je app
st.markdown("## 🏆 Total Ranking European League")
st.caption(f"Laatst bijgewerkt: {last_updated.strftime('%d-%m-%Y %H:%M:%S')}")

st.download_button(
    label="📥 Download CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="totaalstand_EL1_EL8.csv",
    mime="text/csv"
)

# 👁️ Tabelweergave (bijv. met AgGrid of st.table)
from st_aggrid import AgGrid, GridOptionsBuilder

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(resizable=True, wrapText=True, autoHeight=True)
gb.configure_grid_options(domLayout='normal')
AgGrid(df, gridOptions=gb.build(), fit_columns_on_grid_load=True)
