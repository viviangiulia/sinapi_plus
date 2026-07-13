# Converte os dados persistidos em uma instância de Composicao
from app.data_loading import get_database
from app.models import (
    Composicao,
    ComponenteComposicao,
    ItemCatalogo,
    TipoItem,
    Catalogo,
)
from app.exceptions import ComposicaoNaoEncontradaError


class ComposicaoRepository:

    def buscar_composicao(self, codigo: str, catalogo: Catalogo) -> Composicao:

        composicoes_df = get_database(catalogo.nome)

        dados_composicao = composicoes_df.loc[
            composicoes_df["codigo_composicao"] == codigo
        ]

        if dados_composicao.empty:
            raise ComposicaoNaoEncontradaError(
                f"Composição {codigo} não encontrada no catálogo {catalogo.nome}."
            )

        primeira_linha = dados_composicao.iloc[0]

        componentes = []

        for _, linha in dados_composicao.iterrows():

            item = ItemCatalogo(
                codigo=linha["codigo_composicao_secundaria"],
                descricao=linha["descricao_da_composicao_secundaria"],
                tipo=TipoItem(linha["tipo"]),
                catalogo=catalogo,
            )

            componentes.append(
                ComponenteComposicao(
                    item=item,
                    coeficiente=linha["coeficiente"],
                )
            )

        return Composicao(
            codigo=primeira_linha["codigo_composicao"],
            descricao=primeira_linha["descricao_da_composicao"],
            items=componentes,
        )
