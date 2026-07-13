# Converte os dados persistidos em uma instância de PrecoItemCatalogoo
from app.data_loading import get_database
from app.models import PrecoItemCatalogo, ItemCatalogo, FontePrecos, Estado, Competencia
import pandas as pd

class PrecoRepository:

    def buscar_preco(
        self,
        item: ItemCatalogo,
        estado: Estado,
        fonte_precos: FontePrecos,
        competencia: Competencia,
    ) -> PrecoItemCatalogo:

        precos_df = get_database(fonte_precos.nome)

        precos_df["competencia"] = pd.to_datetime(
            precos_df["competencia"]
        )

        dados_item = precos_df.loc[
            (
                precos_df["codigo_da_composicao"]
                == item.codigo
            )
            & (
                precos_df["competencia"]
                == pd.Timestamp(competencia.para_date())
            )
        ]

        if dados_item.empty:
            raise ValueError(
                f"Preço não encontrado para o item {item.codigo}, "
                f"competência {competencia.mes:02d}/{competencia.ano}, "
                f"fonte {fonte_precos.nome}."
            )

        uf = estado.sigla.lower()

        if uf not in dados_item.columns:
            raise ValueError(
                f"Estado {estado.sigla} não disponível "
                f"na fonte de preços {fonte_precos.nome}."
            )

        preco_unitario = dados_item.iloc[0][uf]

        return PrecoItemCatalogo(
            item=item,
            preco_unitario=preco_unitario,
            estado=estado,
            fonte_precos=fonte_precos,
            competencia=competencia,
        )