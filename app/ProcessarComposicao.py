import pandas as pd
import streamlit as st
from typing import Dict, Tuple
from configs.config_agua import CONFIG_AGUA
from configs.config_esgoto import CONFIG_ESGOTO

class InputCollector:
    def __init__(self, session: Dict) -> None:

        for key, value in session.items():
            if key.startswith("input_"):
                # new_key = key.replace("input_", "")
                setattr(self, key, value)

        self.base_composicoes = session["arquivos_base"]["base_composicoes"]
        self.precos_composicoes_insumos = session["arquivos_base"][
            "precos_composicoes_insumos"
        ]


class InputMapper:
    """Resonsável por converter a informação dos inputs em composição e quantidade de forma que permita a precificação do item selecionado pelo usuário."""

    handlers = {}

    @classmethod
    def register(cls, nome_regra):
        """Decorador que adiciona ao handler registry as funções que devem ser executadas com base em cada regra de negócio."""

        def wrapper(func):
            cls.handlers[nome_regra] = func
            return func

        return wrapper

    def __init__(self, collector: InputCollector):
        self.inputs = collector  # valores já limpos da interface

    def converter_categoria(self, config_categoria: Dict) -> list[Dict]:
        """Executa a conversão de todos os inputs da categoria para composições orçamentárias e quantidades.
        Já executa a conversão com base em regras personalizadas utilizando métodos específicos para cada regra.
        """
        itens = []

        for nome_regra, conteudo_regra in config_categoria.items():
            if nome_regra in self.handlers:
                itens += self.handlers[nome_regra](self, conteudo_regra)
            else:
                raise ValueError(f"Regra '{nome_regra}' não possui handler registrado.")

        return itens


@InputMapper.register("simples")
def converter_simples(self, config_simples: Dict) -> list[Dict]:
    """Converte inputs simples retornando um dicionário com o código da composição associada ao item e a quantidade orçada."""
    itens = []
    for nome_input, codigo_composicao in config_simples.items():
        quantidade = getattr(self.inputs, nome_input, 0)
        if quantidade:
            itens.append(
                {
                    "codigo": codigo_composicao,
                    "quantidade": quantidade,
                }
            )
    return itens


@InputMapper.register("redes")
def converter_redes(self, config_redes: Dict) -> list[Dict]:
    """Com base nas informações da rede retorna as informações das composições
    para cada tipo de material e diâmetro.
    """
    itens = []
    for rede, regras in config_redes.items():
        qtd_trechos = getattr(self.inputs, regras["input_qtd"], 0)

        for i in range(qtd_trechos):
            diametro = getattr(self.inputs, f"{regras['input_diametro']}{i}", None)
            comprimento = getattr(self.inputs, f"{regras['input_comprimento']}{i}", 0)

            if diametro in regras["mapa_composicao"]:
                codigo = regras["mapa_composicao"][diametro]
                itens.append(
                    {
                        "codigo": codigo,
                        "quantidade": comprimento,
                    }
                )
    return itens


InputMapper.converter_simples = converter_simples
InputMapper.converter_redes = converter_redes


class Precificador:
    def __init__(
        self, base_composicoes, precos_composicoes_insumos, composicao, estado
    ):
        self.df_base_composicoes = base_composicoes
        self.df_base_precos = precos_composicoes_insumos
        self.codigo_composicao = (
            composicao  # Vem da conversão através de ConverterInputs
        )
        self.estado = estado  # Vem da ColetarInputs

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
    ) -> Tuple[pd.DataFrame, list]:
        """Retorna um dataframe com os custos unitários das composições secundárias
        para o estado selecionado."""

        estado = self.estado.lower()
        df_filtrado = self.df_base_precos[["codigo_da_composicao", estado]].set_index(
            "codigo_da_composicao"
        )

        custos = []
        warnings = []
        for composicao in composicoes_secundarias:
            try:
                custo = df_filtrado.at[composicao, estado]
            except KeyError:
                warnings.append(
                    f"Composição/Insumo {composicao} sem preço para {self.estado}"
                )
                custo = 0
            custos.append({"codigo_composicao_secundaria": composicao, "custo": custo})

        return pd.DataFrame(custos), warnings

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

    def calcular_custo_unitario(
        self,
        composicoes_secundarias,
        custos_composicoes_secundarias,
        indices_composicoes_secundarias,
    ):
        custo_unitario_composicao = self.calcular_custo_unitario_composicao_primaria(
            custos_composicoes_secundarias, indices_composicoes_secundarias
        )
        return custo_unitario_composicao

    def precificar_composicao(self):
        composicoes_secundarias = self.buscar_composicoes_secundarias()
        custos_composicoes_secundarias, warnings = (
            self.buscar_custos_composicoes_secundarias(composicoes_secundarias)
        )
        indices_composicoes_secundarias = self.buscar_indices_composicoes_secundarias()

        custo_unitario_composicao = self.calcular_custo_unitario(
            composicoes_secundarias,
            custos_composicoes_secundarias,
            indices_composicoes_secundarias,
        )
        return custo_unitario_composicao, warnings


class OrcamentoBuilder:

    def __init__(self, session: dict):
        self.session = session

    def montar_orcamento_completo(self):

        user_inputs = InputCollector(self.session)

        categorias = [CONFIG_AGUA, CONFIG_ESGOTO]
        lista_itens_orcamento = []
        mapper = InputMapper(user_inputs)
        for categoria in categorias:
            lista_itens_orcamento.extend(mapper.converter_categoria(categoria))

        estado = user_inputs.input_estado
        base_composicoes = user_inputs.base_composicoes
        precos_composicoes_insumos = user_inputs.precos_composicoes_insumos
        lista_avisos = []
        for item in lista_itens_orcamento:
            codigo_composicao = item["codigo"]
            quantidade = item["quantidade"]
            item["custo_unitario"], warnings = Precificador(
                base_composicoes, precos_composicoes_insumos, codigo_composicao, estado
            ).precificar_composicao()

            item["custo_total"] = quantidade * item["custo_unitario"]
            item["descricao"] = base_composicoes.loc[
                base_composicoes["codigo_composicao"] == codigo_composicao,
                "descricao_da_composicao",
            ].values[0]
            item["unidade"] = base_composicoes.loc[
                (base_composicoes["codigo_composicao"] == codigo_composicao)
                & (base_composicoes["codigo_composicao_secundaria"].isna()),
                "unidade",
            ].values[0]
            lista_avisos.extend(warnings)

        return lista_itens_orcamento, lista_avisos


class OrcamentoAnalyzer:
    def __init__(self, lista_itens):
        self.df = pd.DataFrame(lista_itens)
        self._preparar_categoria()

    def _preparar_categoria(self):
        self.df["categoria"] = self.df["codigo"].apply(
            lambda x: "Água" if "AGUA" in x.upper() else "Esgoto"
        )

    def get_dataframe(self):

        rename_map = {
            "codigo": "Código Composição",
            "quantidade": "Quantidade",
            "custo_unitario": "Custo Unitário (R$)",
            "custo_total": "Custo Total (R$)",
            "descricao": "Descrição Composição",
            "unidade": "Unidade",
        }

        self.df = self.df.rename(columns=rename_map)

        colunas_ordenadas = [
            "Código Composição",
            "Descrição Composição",
            "Unidade",
            "Quantidade",
            "Custo Unitário (R$)",
            "Custo Total (R$)",
        ]

        colunas_existentes = [c for c in colunas_ordenadas if c in self.df.columns]

        df_formatado = self.df[colunas_existentes].copy()

        if "Custo Unitário (R$)" in df_formatado:
            df_formatado["Custo Unitário (R$)"] = (
                df_formatado["Custo Unitário (R$)"].astype(float).round(2)
            )

        if "Custo Total (R$)" in df_formatado:
            df_formatado["Custo Total (R$)"] = (
                df_formatado["Custo Total (R$)"].astype(float).round(2)
            )

        return df_formatado

    def obter_totais_por_categoria(self):
        return self.df.groupby("categoria")["custo_total"].sum().reset_index()

    def total_geral(self):
        return self.df["custo_total"].sum().round(2)
