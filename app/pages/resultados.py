import streamlit as st
from utils import calcular_custo_total, montar_relatorio_final, criar_relatorio_excel
import pandas as pd


st.subheader("Resultados da Simulação")

_, __, coluna = st.columns([3, 1, 1])
custo_total = calcular_custo_total()
with coluna:
    st.metric(
        "Total Simulado (R$)",
        custo_total,
    )


df_final = montar_relatorio_final()
with st.container(border=True):
    st.subheader("Relatório do Orçamento")
    st.dataframe(df_final)

if not df_final.empty:
    if st.button("Gerar Relatório Excel"):
        try:
            with st.spinner("Processando Resultados...."):
                buffer, nome_arquivo = criar_relatorio_excel(
                    df_final, "Relatório Orçamento"
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
