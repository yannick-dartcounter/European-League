import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="European League Ranking", layout="wide")
st.title("🏆 Total Ranking European League")

url = "https://raw.githubusercontent.com/yannick-dartcounter/European-League/main/totaalstand_EL1_EL8.xlsx"

@st.cache_data(ttl=1)
def laad_excel_van_github(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_excel(BytesIO(response.content))

        last_modified = response.headers.get("Last-Modified")
        last_updated = None
        if last_modified:
            last_updated = datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S %Z")

        return df, last_updated
    except Exception as e:
        st.error(f"❌ Fout bij laden Excelbestand:\n\n{e}")
        return None, None

# Data laden
df, last_updated = laad_excel_van_github(url)

if df is not None:
    if last_updated:
        st.caption(f"📅 Laatst bijgewerkt: {last_updated.strftime('%d-%m-%Y %H:%M:%S')} UTC")

    # ❌ Verwijder indexkolom (indien aanwezig)
    df.reset_index(drop=True, inplace=True)

    # 🔧 AgGrid configureren
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, wrapText=True, autoHeight=True)
    gb.configure_grid_options(domLayout='normal')  # of 'autoHeight'
    gb.configure_columns(df.columns.tolist(), cellStyle={'textAlign': 'center'})
    gb.configure_side_bar(False)
    gb.configure_pagination(paginationAutoPageSize=True)

    grid_options = gb.build()

    # ✅ AgGrid renderen
    AgGrid(
        df,
        gridOptions=grid_options,
        height=600,
        theme="balham",  # andere opties: "material", "streamlit", "balham-dark"
        fit_columns_on_grid_load=True,
        reload_data=True
    )

    # 📥 Downloadknop
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "ranking_european_league.csv", "text/csv")

else:
    st.warning("⚠️ Kon totaalstand niet laden van GitHub.")
