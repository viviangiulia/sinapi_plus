from ProcessarComposicao import PrecificarComposicao
import pandas as pd
from io import BytesIO
import datetime


def calcular_custo_total() -> float:
    """Retorna o custo total da simulação."""

    dicionario_composicoes = PrecificarComposicao.dicionario_resultante
    total_simulado = 0
    for _, dic in dicionario_composicoes.items():
        total_simulado += dic["custo_total"]
    return round(total_simulado, 2)


def calcular_custo_categoria(escopo: str) -> float:
    """Retorna o custo simulado de uma determinada categoria de infraestrutura."""
    dicionario_composicoes = PrecificarComposicao.dicionario_resultante
    total_simulado = 0
    for _, dic in dicionario_composicoes.items():
        if dic["_escopo"] == escopo:
            total_simulado += dic["custo_total"]
    return float(total_simulado)


def calcular_custo_composicao(
    session, escopo: str, dicionario_composicoes: dict
) -> None:
    """Processa as composições e calcula o preço unitário e custo total."""
    for composicao, quantidade in dicionario_composicoes.items():
        PrecificarComposicao(session, composicao, quantidade, escopo).gerar_resultado()


def gerar_dicionario_trechos_rede(
    session,
    chave_qtd_trechos: str,
    prefixo_diametro_rede: str,
    prefixo_comprimento_rede: str,
    composicoes_rede: dict,
) -> dict:
    """Retonar um dicionário com o código da composição e a chave para acessar a quantidade simulada."""
    dicionario_iteravel = {}
    qtd_trechos = session[chave_qtd_trechos]
    tipo_rede = chave_qtd_trechos.split("_")[-1]
    for trecho in range(qtd_trechos):
        diametro_trecho = session[f"{prefixo_diametro_rede}{trecho + 1}"]
        composicao_trecho = composicoes_rede[tipo_rede][diametro_trecho]
        dicionario_iteravel[composicao_trecho] = (
            f"{prefixo_comprimento_rede}{trecho + 1}"
        )

    return dicionario_iteravel


def montar_relatorio_final():
    dicionario_composicoes = PrecificarComposicao.dicionario_resultante
    try:
        df_final = pd.DataFrame.from_dict(dicionario_composicoes, orient="index")
        df_final = df_final[
            [
                "_escopo",
                "descricao",
                "unidade",
                "quantidade",
                "custo_unitario",
                "custo_total",
            ]
        ]
        df_final = df_final.loc[df_final["custo_total"] > 0].reset_index(drop=True)
        df_final["custo_unitario"] = df_final["custo_unitario"].round(2)
        df_final["custo_total"] = df_final["custo_total"].round(2)

        df_final = df_final.rename(
            columns={
                "custo_unitario": "Custo Unitário (R$)",
                "custo_total": "Custo Total (R$)",
                "quantidade": "Quantidade",
                "descricao": "Descrição",
                "unidade": "Unidade",
                "_escopo": "Escopo",
            }
        )
    except:
        df_final = pd.DataFrame(
            columns=(
                "Escopo",
                "Descrição",
                "Unidade",
                "Quantidade",
                "Custo Unitário (R$)",
                "Custo Total (R$)",
            )
        )

    return df_final


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
