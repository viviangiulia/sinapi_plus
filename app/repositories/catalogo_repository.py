from app.data_loading import get_database
from app.models import ElementoQuantificavel,ComposicaoQuantificada


class CatalogoRepository:

    def buscar_codigo_composicao(
        self, elemento: ElementoQuantificavel
    ) -> ComposicaoQuantificada:

        catalogo_elementos_df = get_database("catalogo_elementos")

        df_filtrado = catalogo_elementos_df.loc[
            catalogo_elementos_df["categoria"] == elemento.categoria
        ]

        
        for atributo, valor in vars(elemento.especificacao).items():

            if valor is None:
                continue

            df_filtrado = df_filtrado.loc[
                df_filtrado[atributo] == valor
            ]

        if df_filtrado.empty:
            raise ValueError(
                f"Nenhuma composição encontrada para o elemento {elemento}."
            )

        if len(df_filtrado) > 1:
            raise ValueError(
                f"Mais de uma composição encontrada para o elemento {elemento}."
            )

        codigo = df_filtrado["codigo_composicao"].iloc[0]

        return ComposicaoQuantificada(
            codigo_composicao=codigo,
            quantidade=elemento.quantidade,
        )