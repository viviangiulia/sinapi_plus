import pandas as pd
from collections import defaultdict
import streamlit as st


class PrecificarComposicao:
    """Processa cada composição cadastrada na base de códigos.
    Com base nos inputs do usuário (estado e quantidade) realiza a precificação da composição.
    """

    dicionario_resultante = {}
    _processados_no_rerun = defaultdict(set)

    def __init__(self, session, codigo_composicao, quantidade, escopo="_default"):
        self.session = session
        self.estado = session.get("input_estado", "SP")
        self.codigo_composicao = codigo_composicao
        self.quantidade_composicao = session.get(quantidade, 0)
        self.escopo = escopo
        self.df_base_composicoes = self.session["arquivos_base"]["base_composicoes"]
        self.df_base_precos = self.session["arquivos_base"][
            "precos_composicoes_insumos"
        ]
        self.descricao_composicao = self.df_base_composicoes.loc[
            self.df_base_composicoes["codigo_composicao"] == self.codigo_composicao,
            "descricao_da_composicao",
        ].values[0]
        self.unidade = self.df_base_composicoes.loc[
            (self.df_base_composicoes["codigo_composicao"] == self.codigo_composicao)
            & (self.df_base_composicoes["codigo_composicao_secundaria"].isna()),
            "unidade",
        ].values[0]

    @classmethod
    def iniciar_sincronizacao(cls, escopo="_default"):
        cls._processados_no_rerun[escopo].clear()

    @classmethod
    def finalizar_sincronizacao(cls, escopo="_default"):
        validas = cls._processados_no_rerun[escopo]
        for k in list(cls.dicionario_resultante.keys()):
            if (
                cls.dicionario_resultante[k].get("_escopo") == escopo
                and k not in validas
            ):
                del cls.dicionario_resultante[k]

    def buscar_composicoes_secundarias(self) -> list:
        """Retorna a lista de códigos de composições ou insumos secundários
        que compõem a composição primária.

        Retornos:
            list: Lista de códigos das composições secundárias."""

        composicoes_secundarias = (
            self.df_base_composicoes.loc[
                self.df_base_composicoes["codigo_composicao"] == self.codigo_composicao,
                "codigo_composicao_secundaria",
            ]
            .dropna()
            .tolist()
        )

        return composicoes_secundarias

    def buscar_indices_composicoes_secundarias(self) -> pd.DataFrame:
        """Retonar um dataframe com cada composição secundária e seu coeficiente."""

        df_filtrado = self.df_base_composicoes[
            ["codigo_composicao", "codigo_composicao_secundaria", "coeficiente"]
        ]
        return df_filtrado.loc[
            (df_filtrado["codigo_composicao"] == self.codigo_composicao)
            & (df_filtrado["codigo_composicao_secundaria"].notna()),
            ["codigo_composicao_secundaria", "coeficiente"],
        ].reset_index(drop=True)

    def buscar_custos_composicoes_secundarias(
        self, composicoes_secundarias: list
    ) -> pd.DataFrame:
        """Retorna um dataframe com os custos unitários das composições secundárias
        para o estado selecionado."""

        estado = self.estado.lower()
        df_filtrado = self.df_base_precos[["codigo_da_composicao", estado]].set_index(
            "codigo_da_composicao"
        )

        custos = []
        for composicao in composicoes_secundarias:
            try:
                custo = df_filtrado.at[composicao, estado]
            except KeyError:
                st.warning(
                    f"Composição/Insumo {composicao} sem preço para {self.estado}"
                )
                custo = 0
            custos.append({"codigo_composicao_secundaria": composicao, "custo": custo})

        return pd.DataFrame(custos)

    def calcular_custo_unitario_composicao_primaria(
        self,
        custos_unitarios_composicoes_secundarias: pd.DataFrame,
        indices_composicoes_secundarias: pd.DataFrame,
    ) -> float:
        """Retonar o custo unitário da composição primária."""

        df = custos_unitarios_composicoes_secundarias.merge(
            indices_composicoes_secundarias,
            on="codigo_composicao_secundaria",
            how="inner",
        )
        return (df["custo"] * df["coeficiente"]).sum()

    def gerar_resultado(self):
        """Adiciona o resultado ao dicionário as seguintes informações:
        - Composição Selecionada
        - Quantidade Orçada
        - Custo Unitário (regionalizado)
        - Estado considerado na precificação
        - Custo Total
        - Escopo
        """
        composicoes_secundarias = self.buscar_composicoes_secundarias()
        custos_composicoes_secundarias = self.buscar_custos_composicoes_secundarias(
            composicoes_secundarias
        )
        indices_composicoes_secundarias = self.buscar_indices_composicoes_secundarias()
        custo_unitario_composicao = self.calcular_custo_unitario_composicao_primaria(
            custos_composicoes_secundarias, indices_composicoes_secundarias
        )

        custo_total_composicao = custo_unitario_composicao * self.quantidade_composicao

        chave = self.codigo_composicao

        self.__class__.dicionario_resultante[chave] = {
            "custo_unitario": float(custo_unitario_composicao),
            "custo_total": float(custo_total_composicao),
            "quantidade": self.quantidade_composicao,
            "codigo_base": self.codigo_composicao,
            "descricao": self.descricao_composicao,
            "unidade":self.unidade,
            "estado": self.estado,
            "_escopo": self.escopo,
        }

        self.__class__._processados_no_rerun[self.escopo].add(chave)

        return self.__class__.dicionario_resultante
