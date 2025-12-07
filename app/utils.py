from ProcessarComposicao import OrcamentoBuilder
import pandas as pd
from io import BytesIO
import datetime
import streamlit as st


def criar_relatorio_excel(df, nome_arquivo="Relatório SINAPI+"):

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Orçamento", index=False)

        workbook = writer.book
        worksheet = writer.sheets["Orçamento"]

        header_format = workbook.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "valign": "top",
                "fg_color": "#006B3F",
                "font_color": "white",
                "border": 1,
            }
        )

        header_format = workbook.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "valign": "top",
                "fg_color": "#006B3F",
                "font_color": "white",
                "border": 1,
            }
        )

        cell_format = workbook.add_format({"border": 1, "text_wrap": True})

        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        for i, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
            worksheet.set_column(i, i, min(max_len, 50))

    buffer.seek(0)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_completo = f"{nome_arquivo}_{timestamp}.xlsx"
    return buffer, nome_completo


@st.cache_data
def calcular_orcamento(session_dict):
    return OrcamentoBuilder(session_dict).montar_orcamento_completo()
