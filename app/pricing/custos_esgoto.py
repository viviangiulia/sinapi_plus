import streamlit as st
from ProcessarComposicao import PrecificarComposicao
from utils import calcular_custo_composicao, gerar_dicionario_trechos_rede


def custo_total_esgoto(escopo):
    """Precifica todas as composições pertinentes a categoria de Esgoto Sanitário."""
    session = st.session_state

    PrecificarComposicao.iniciar_sincronizacao(escopo)

    itens_comuns = {
        "COMP-ESGOTO-006": "input_esgoto_qtd_ligacao_4m",
        "COMP-ESGOTO-008": "input_esgoto_qtd_ligacao_6m",
        "COMP-ESGOTO-003": "input_esgoto_pv_max_150",
        "COMP-ESGOTO-007": "input_esgoto_pv_max_200",
        "COMP-ESGOTO-004": "input_esgoto_pv_max_250",
        "COMP-ESGOTO-005": "input_esgoto_pv_max_300",
    }

    calcular_custo_composicao(session, escopo, itens_comuns)

    composicoes_rede_esgoto = {
        "ocre": {
            100: "COMP-ESGOTO-009",
            150: "COMP-ESGOTO-010",
            200: "COMP-ESGOTO-011",
            250: "COMP-ESGOTO-012",
            300: "COMP-ESGOTO-013",
            350: "COMP-ESGOTO-014",
        },
    }

    dicionario_rede_pvc_ocre = gerar_dicionario_trechos_rede(
        session,
        "input_esgoto_qtd_trechos_ocre",
        "input_esgoto_diametro_ocre_",
        "input_esgoto_comprimento_ocre_",
        composicoes_rede_esgoto,
    )

    calcular_custo_composicao(session, escopo, dicionario_rede_pvc_ocre)
