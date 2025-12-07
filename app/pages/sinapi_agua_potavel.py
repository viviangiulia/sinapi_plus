import streamlit as st
from ProcessarComposicao import OrcamentoAnalyzer
from utils import calcular_orcamento

resultados_orcamento, avisos = calcular_orcamento(dict(st.session_state))
df_custo_categoria = OrcamentoAnalyzer(
    resultados_orcamento
).obter_totais_por_categoria()

session = st.session_state
_, __, coluna = st.columns([3, 1, 1])
escopo = "Água Potável"

tab1, tab2, tab3 = st.tabs(
    ["Ligação Predial e Hidrômetro", "Rede em PBA", "Rede em PVC DEFOFO"]
)


with tab1:
    c1, c2 = st.columns((1, 1))
    with c1:
        st.subheader("Ligação Predial")
        st.info(
            """

        - Rede 50 mm
        - Ramal predial em PEAD de 20 mm
        - Distância até o hidrômetro = 6,0 m
        - Incluso caixa para abrigo do hidrômetro e kit cavalete
        - Não incluso hidrõmetro
        """
        )

        st.number_input(
            "Quantidade de Ligações Prediais (un)",
            min_value=0,
            step=1,
            key="input_agua_ligacao_predial",
        )

    with c2:
        st.subheader("Hidrômetro")
        st.info(
            """

        - Diâmetro Nominal 20 (1/2")
        - Vazão Nominal 1,5 m³/h
        - Fornecimento e Instalação
        """
        )

        st.number_input(
            "Quantidade de Hidrômetros (un)",
            min_value=0,
            step=1,
            key="input_agua_hidrometro",
        )
    st.markdown("---")

with tab2:
    st.subheader("Rede com tubo PBA")
    st.info(
        """
    - Escavação e reaterro
    - Fornecimento e assentamento
    """
    )

    st.number_input(
        label="Quantidade de Trechos de Tubulação (un)",
        min_value=0,
        step=1,
        max_value=3,
        key="input_agua_qtd_trechos_pba",
    )

    for trecho in range(session["input_agua_qtd_trechos_pba"]):
        col1, col2 = st.columns((1, 1))
        with col1:
            st.selectbox(
                f"Diâmetro do Trecho {trecho + 1} (mm)",
                options=[50, 75, 100],
                key=f"input_agua_diametro_pba_{trecho + 1}",
            )

        with col2:
            st.number_input(
                f"Comprimento do Trecho {trecho + 1} (m)",
                min_value=0.0,
                key=f"input_agua_comprimento_pba_{trecho + 1}",
            )

    st.markdown("---")
with tab3:

    st.subheader("Rede com tubo PVC DEFOFO")
    st.info(
        """
    - Escavação e reaterro
    - Fornecimento e assentamento
    """
    )

    st.number_input(
        label="Quantidade de Trechos de Tubulação (un)",
        min_value=0,
        step=1,
        max_value=5,
        key="input_agua_qtd_trechos_defofo",
    )

    for trecho in range(session["input_agua_qtd_trechos_defofo"]):
        col_1, col_2 = st.columns((1, 1))
        with col_1:
            st.selectbox(
                f"Diâmetro do Trecho {trecho + 1} (mm)",
                options=[150, 200, 250, 300],
                key=f"input_agua_diametro_defofo_{trecho + 1}",
            )

        with col_2:
            st.number_input(
                f"Comprimento do Trecho {trecho + 1} (m)",
                min_value=0.0,
                key=f"input_agua_comprimento_defofo_{trecho + 1}",
            )

with coluna:

    custo_total_agua = df_custo_categoria.query("categoria == 'Água'")[
        "custo_total"
    ].sum()
    st.metric(
        "Total (R$) - Água Potável",
        round(custo_total_agua, 2),
    )
