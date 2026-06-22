# Converte os dados persistidos em uma instância de PrecoItemCatalogoo
from data_loading import get_database
from models import PrecoItemCatalogo, ItemCatalogo, TipoItem, Estado


class PrecoRepository:

    def buscar_preco(self, item: ItemCatalogo, estado: Estado) -> PrecoItemCatalogo:
        precos_df = get_database("precos_composicoes_insumos")

        codigo_item = item.codigo

        uf = estado.sigla.lower()

        dados_item = precos_df.loc[
            (precos_df["codigo_da_composicao"] == codigo_item), uf
        ]

        if not dados_item.empty:
            preco_unit = dados_item.iloc[0]

        else:
            raise ValueError(
                f"Preço não encontrado no estado {estado.sigla} para o item {item.codigo}"
            )

        return PrecoItemCatalogo(item=item, estado=estado, preco_unitario=preco_unit)
