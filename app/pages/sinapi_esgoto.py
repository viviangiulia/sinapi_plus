import streamlit as st
from pricing.custos_esgoto import custo_total_esgoto
from ProcessarComposicao import PrecificarComposicao
from utils import calcular_custo_categoria

session = st.session_state
_, __, coluna = st.columns([3, 1, 1])
escopo = "Esgoto Sanitário"

tab1, tab2, tab3 = st.tabs(
    [
        "Ligação Predial de Esgoto",
        "Rede em PVC OCRE",
        "Poços de Visita",
    ]
)

with tab1:
    st.subheader("Ligação Predial de Esgoto")
    st.info(
        """
    - Diâmetro Nominal da Rede 150 mm
    - Diâmetro Nominal do Coletor Predial 100 mm
    - Não incluso caixa de inspeção
            """
    )

    col1, col2 = st.columns((1, 1))

    with col1:
        st.number_input(
            label="Quantidade de ligações - Distância até a caixa de inspeção 4,0 m (un)",
            min_value=0,
            step=1,
            key="input_esgoto_qtd_ligacao_4m",
        )

    with col2:
        st.number_input(
            label="Quantidade de ligações - Distância até a caixa de inspeção 6,0 m (un)",
            min_value=0,
            step=1,
            key="input_esgoto_qtd_ligacao_6m",
        )

with tab2:
    st.subheader("Rede com Tubo PVC OCRE")
    st.info(
        """
    - Escavação e reaterro
    - Fornecimento e assentamento
            """
    )

    st.number_input(
        label="Quantidade de Trechos de Tubulação (un)",
        min_value=0,
        max_value=7,
        key="input_esgoto_qtd_trechos_ocre",
    )

    col_1, col_2 = st.columns((1, 1))

    for trecho in range(session["input_esgoto_qtd_trechos_ocre"]):
        with col_1:
            st.selectbox(
                label=f"Diâmetro do Trecho {trecho + 1} (mm)",
                options=[100,150, 200, 250, 300, 350, 400],
                key=f"input_esgoto_diametro_ocre_{trecho + 1}",
            )

        with col_2:
            st.number_input(
                label=f"Comprimento do Trecho {trecho + 1} (m)",
                min_value=0.0,
                key=f"input_esgoto_comprimento_ocre_{trecho + 1}",
            )

with tab3:
    st.subheader("Poços de Visita")
    st.info(
        """
    - Poço de Visita em Concreto Pré-moldado
    - Diâmetro Interno 1 m
    - Inclui tampão simples com base
    """
    )
    col__1, col__2 = st.columns((1, 1))

    with col__1:
        st.number_input(
            "Poço de Visita - Profundidade até 1,50 m (un)",
            min_value=0,
            step=1,
            key="input_esgoto_pv_max_150",
        )

        st.number_input(
            "Poço de Visita - Profundidade entre 2,00 e 2,50 m (un)",
            min_value=0,
            step=1,
            key="input_esgoto_pv_max_250",
        )

    with col__2:
        st.number_input(
            "Poço de Visita - Profundidade entre 1,50 e 2,00 m (un)",
            min_value=0,
            step=1,
            key="input_esgoto_pv_max_200",
        )

        st.number_input(
            "Poço de Visita - Profundidade entre 2,50 e 3,00 m (un)",
            min_value=0,
            step=1,
            key="input_esgoto_pv_max_300",
        )

PrecificarComposicao.finalizar_sincronizacao(escopo)
custo_total_esgoto(escopo)
with coluna:
    custo_total_escopo = calcular_custo_categoria(escopo)
    st.metric(
        "Total (R$) - Esgoto Sanitário",
        round(custo_total_escopo, 2),
    )
