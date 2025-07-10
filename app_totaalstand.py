import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(page_title="European League Ranking", layout="wide")
st.title("🏆 Totale Ranking European League")

# 📁 URL naar Excelbestand op GitHub
url = "https://raw.githubusercontent.com/yannick-dartcounter/European-League/main/totaalstand_EL1_EL8.xlsx"

# 📥 Cache het ophalen van het Excelbestand
@st.cache_data(ttl=300)
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

# 📊 Laad de data
df, last_updated = laad_excel_van_github(url)

if df is not None:
    # 📅 Laatst bijgewerkt tonen
    if last_updated:
        st.caption(f"📅 Laatst bijgewerkt: {last_updated.strftime('%d-%m-%Y %H:%M:%S')} UTC")

    # 🔢 Index verwijderen uit weergave
    df.reset_index(drop=True, inplace=True)

    # 🔧 AgGrid instellingen
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, cellStyle={"textAlign": "center"})
    gb.configure_grid_options(domLayout='autoHeight')  # 👉 Laat de grid automatisch in hoogte meegroeien
    gb.configure_side_bar(False)
    gb.configure_pagination(enabled=False)

    grid_options = gb.build()

    # 🧠 JavaScript om kolommen automatisch te resizen op basis van inhoud
    auto_size_js = JsCode("""
        function(e) {
            setTimeout(function() {
                e.api.sizeColumnsToFit();
            }, 100);
        };
    """)

    # 📈 Toon de tabel
    AgGrid(
        df,
        gridOptions=grid_options,
        theme="balham",
        allow_unsafe_jscode=True,
        custom_js={"onFirstDataRendered": auto_size_js},
        reload_data=True,
        height=None,  # ➕ Geen onnodige witruimte
        fit_columns_on_grid_load=False
    )

    # 📤 Downloadknop
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "ranking_european_league.csv", "text/csv")
else:
    st.warning("⚠️ Kon totaalstand niet laden van GitHub.")
