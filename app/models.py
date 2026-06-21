import pytest
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


@dataclass(frozen=True)
class Tubulacao:
    material: str  # TODO deve vir da lista de materiais disponíveis para cada rede
    diametro: int  # TODO deve vir da lista de diâmetros disponíveis para cada material


@dataclass
class TrechoRede:
    id: int
    tubulacao: Tubulacao
    comprimento: float = 0.0

    def check_valid_length(self):
        if self.comprimento < 0:
            raise ValueError("O comprimento do trecho não pode ser negativo.")

    def __post_init__(self):
        self.check_valid_length()


@dataclass
class ComposicaoQuantificada:
    codigo_composicao: str
    quantidade: float

    def __post_init__(self):
        if self.quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa.")


@dataclass(frozen=True)
class Especificacao:
    material: str | None = None
    diametro: int | None = None
    profundidade: float | None = None


@dataclass
class ElementoQuantificavel:
    categoria: str
    quantidade: float
    especificacao: Especificacao

    def __post_init__(self):
        if self.quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa.")


class Rede:
    def __init__(self, escopo_rede: str, trechos: List[TrechoRede]):
        self.escopo_rede = escopo_rede  # TODO deve ser um Enum das redes disponíveis (Água, Esgoto, Drenagem)
        self.trechos = trechos

    @property
    def comprimentos_rede_por_tubulacao(self) -> Dict[Tubulacao, float]:
        totais = {}

        for trecho in self.trechos:
            totais.setdefault(trecho.tubulacao, 0)
            totais[trecho.tubulacao] += trecho.comprimento

        return totais

    def gerar_elementos_quantificaveis(self) -> List[ElementoQuantificavel]:
        lista_elementos = []

        for tubulacao, quantidade in self.comprimentos_rede_por_tubulacao.items():
            lista_elementos.append(
                ElementoQuantificavel(
                    categoria="TUBULACAO",
                    quantidade=quantidade,
                    especificacao=Especificacao(
                        material=tubulacao.material,
                        diametro=tubulacao.diametro,
                    ),
                )
            )

        return lista_elementos

class TipoItem(Enum):
    INSUMO = "Insumo"
    COMPOSICAO = "Composição"

@dataclass
class ItemCatalogo:
    codigo: str
    descricao: str
    tipo:TipoItem

    def __post_init__(self):
        if not self.codigo:
            raise ValueError(""
            "Um Item do Catálogo não pode ter código vazio.")

@dataclass
class ComponenteComposicao:
    item: ItemCatalogo
    coeficiente: float

    def __post_init__(self):
        if self.coeficiente < 0:
            raise ValueError(
                "Coeficiente não pode ser negativo."
            )

@dataclass
class Composicao:
    codigo: str
    descricao: str
    items: List[ComponenteComposicao]

    def __post_init__(self):
        if not self.items:
            raise ValueError(
                "Composição precisa obrigatoriamente de ter itens associados."
            )
        

@dataclass(frozen=True)
class Estado:
    sigla: str

@dataclass
class PrecoItemCatalogo:
    item: ItemCatalogo
    estado: Estado
    preco_unitario: float

    def __post_init__(self):
        if self.preco_unitario < 0:
            raise ValueError("Preço não pode ser negativo.")
        


@dataclass
class ComponentePrecificado:
    componente: ComponenteComposicao
    preco_unitario: float

    @property
    def custo_unitario(self):
        return (
            self.componente.coeficiente
            * self.preco_unitario
        )
    
@dataclass
class ComposicaoPrecificada:
    codigo: str
    estado: Estado
    quantidade: float
    componentes: List[ComponentePrecificado]

    @property
    def custo_unitario(self):
        return sum(
            componente.custo_unitario
            for componente in self.componentes
        )

    @property
    def custo_total(self):
        return self.custo_unitario * self.quantidade