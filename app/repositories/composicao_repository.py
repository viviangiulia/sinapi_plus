# Converte os dados persistidos em uma instância de Composicao
from app.data_loading import get_database
from app.models import Composicao, ComponenteComposicao, ItemCatalogo,TipoItem

class ComposicaoRepository:

    def buscar_composicao(self, codigo: str) -> Composicao:

        composicoes_df = get_database("base_composicoes_v2")

        dados_composicao = composicoes_df.loc[
            composicoes_df["codigo_composicao"] == codigo
        ]

        primeira_linha = dados_composicao.iloc[0]

        componentes = []

        for _, linha in dados_composicao.iterrows():

            item = ItemCatalogo(
                codigo=linha["codigo_composicao_secundaria"],
                descricao=linha["descricao_da_composicao_secundaria"],
                tipo=TipoItem(linha["tipo"]),
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


