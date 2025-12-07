import streamlit as st
from utils import criar_relatorio_excel
from ProcessarComposicao import OrcamentoAnalyzer
from utils import calcular_orcamento

resultados_orcamento, avisos = calcular_orcamento(dict(st.session_state))
df_resultados = OrcamentoAnalyzer(resultados_orcamento).get_dataframe()

st.subheader("Resultados da Simulação")

_, __, coluna = st.columns([3, 1, 1])
custo_total = OrcamentoAnalyzer(resultados_orcamento).total_geral()
with coluna:
    st.metric(
        "Total Simulado (R$)",
        custo_total,
    )


with st.container(border=True):
    st.subheader("Relatório do Orçamento")
    st.dataframe(df_resultados)

if not df_resultados.empty:
    if st.button("Gerar Relatório Excel"):
        try:
            with st.spinner("Processando Resultados...."):
                buffer, nome_arquivo = criar_relatorio_excel(
                    df_resultados, "Relatório Orçamento"
                )

                st.download_button(
                    label="Baixar Relatório Excel",
                    data=buffer,
                    file_name=nome_arquivo,
                    mime="application/vnd.ms-excel",
                    help="Clique para baixar o relatório em formato Excel",
                )

                st.success(
                    "✅ Relatório gerado com sucesso! Clique no botão acima para baixar."
                )

        except Exception as e:
            st.error(f"❌ Erro ao gerar relatório: {e}")
