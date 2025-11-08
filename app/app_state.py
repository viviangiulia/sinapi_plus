import streamlit as st
import re


def initial_session_state():
    """Inicializa o session_state setando valores defalt para as chaves necessárias."""
    defaults = {
        "loaded_data": False,
        "input_estado": "SP",
        "input_agua_ligacao_predial": 0,
        "input_agua_hidrometro": 0,
        "input_agua_qtd_trechos_pba": 0,
        "input_agua_qtd_trechos_defofo": 0,
        "input_esgoto_qtd_ligacao_4m":0,
        "input_esgoto_qtd_ligacao_6m":0,
        "input_esgoto_qtd_trechos_ocre":0,
        "input_esgoto_pv_max_150":0,
        "input_esgoto_pv_max_250":0,
        "input_esgoto_pv_max_200":0,
        "input_esgoto_pv_max_300":0,
    }

    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def persist_state():
    """Mantém os valores dos widgets salvos no session_state em todas as páginas."""

    persistent_keys = [
        "loaded_data",
        "input_estado",
        "input_agua_ligacao_predial",
        "input_agua_hidrometro",
        "input_agua_qtd_trechos_pba",
        "input_agua_diametro_pba_#",
        "input_agua_comprimento_pba_#",
        "input_agua_qtd_trechos_defofo_#",
        "input_agua_diametro_defofo_#",
        "input_agua_comprimento_defofo_#",
        "input_esgoto_qtd_ligacao_4m",
        "input_esgoto_qtd_ligacao_6m",
        "input_esgoto_qtd_trechos_ocre",
        "input_esgoto_diametro_ocre_#",
        "input_esgoto_comprimento_ocre_#",
        "input_esgoto_pv_max_150",
        "input_esgoto_pv_max_200",
        "input_esgoto_pv_max_250",
        "input_esgoto_pv_max_300",
    ]

    for key in persistent_keys:
        if key.endswith("#"):
            padrao = r"#"
            persistent_keys.extend([re.sub(padrao, str(i), key) for i in range(1, 11)])
            persistent_keys.remove(key)
            
        if key in st.session_state:
            st.session_state[key] = st.session_state[key]
