import streamlit as st
from data_loading import carregar_arquivos
from app_state import initial_session_state, persist_state

st.set_page_config(
    page_title="SINAPI+",
    layout="wide",
    initial_sidebar_state="expanded",
)

initial_session_state()
persist_state()

if not st.session_state.loaded_data:
    try:
        carregar_arquivos()

    except Exception as e:
        st.error(f"Erro ao carregar os arquivos: {e}.")
        st.stop()

home = st.Page(page="pages/home.py", title="Home", icon=":material/home:", default=True)
agua_potavel = st.Page(
    page="pages/sinapi_agua_potavel.py",
    title="Água Potável",
    icon=":material/water_drop:",
)
esgoto = st.Page(
    page="pages/sinapi_esgoto.py",
    title="Esgoto Sanitário",
    icon=":material/water_pump:",
)
resultados = st.Page(
    page="pages/resultados.py", title="Resultados", icon=":material/receipt_long:"
)
pages = [home, agua_potavel, esgoto, resultados]

selected_page = st.navigation(pages)
selected_page.run()
