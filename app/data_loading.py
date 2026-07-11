import streamlit as st
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
EXCEL_DIR = BASE_DIR / "excel_files"


def get_database(nome_arquivo: str) -> pd.DataFrame:
    return pd.read_excel(EXCEL_DIR / f"{nome_arquivo}.xlsx")
# @st.cache_data(ttl=600, show_spinner=False)
# def get_database(nome_arquivo: str):
#     return pd.read_excel(f'excel_files/{nome_arquivo}.xlsx')

def carregar_arquivos():
    with st.spinner("Os arquivos estão sendo carregados, aguarde..."):
        st.session_state.setdefault("arquivos_base", {})
        progress_placeholder = st.empty()
        progress = 0
        arquivos_base = [
            "precos_composicoes_insumos",
            "base_composicoes"
        ]
        for arquivo in arquivos_base:
            st.session_state["arquivos_base"][arquivo] = get_database(arquivo)
            progress += 50
            progress_placeholder.progress(progress)
        
        progress_placeholder.empty()
    st.session_state["loaded_data"] = True

