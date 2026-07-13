from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
from datetime import date
from decimal import Decimal

@dataclass(frozen=True)
class Especificacao:
    "Define o conjunto de características associadas um insumo específico."
    material: str | None = None
    diametro: int | None = None
    profundidade: float | None = None

    def __post_init__(self):
        if self.diametro and self.diametro < 0:
            raise ValueError("Diâmetro não pode ser negativo.")
        
        if self.profundidade and self.profundidade < 0:
            raise ValueError("Profundidade não pode ser negativa.")


@dataclass(frozen=True)
class Tubulacao:
    material: str  # TODO deve vir da lista de materiais disponíveis para cada rede
    diametro: int  # TODO deve vir da lista de diâmetros disponíveis para cada material

    def __post_init__(self):
        if self.diametro < 0:
            raise ValueError("Diâmetro não pode ser negativo.")


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


class TipoItem(Enum):
    INSUMO = "Insumo"
    COMPOSICAO = "Composição"


@dataclass(frozen=True)
class FontePrecos:
    """A base que é utilizada como referência de preços"""
    codigo: str
    nome: str


@dataclass(frozen=True)
class Catalogo:
    """A base que concentra as informações de composições e insumos"""
    codigo: str
    nome: str

@dataclass
class ComposicaoQuantificada:
    codigo_composicao: str
    catalogo: Catalogo
    quantidade: float

    def __post_init__(self):
        if self.quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa.")

@dataclass(frozen=True)
class ItemCatalogo:
    codigo: str
    descricao: str
    tipo: TipoItem
    catalogo: Catalogo

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

@dataclass(frozen=True)
class Competencia:
    ano: int
    mes: int

    def __post_init__(self):
        if not 1 <= self.mes <= 12:
            raise ValueError(
                "O mês da competência deve estar entre 1 e 12."
            )

    def para_date(self) -> date:
        return date(self.ano, self.mes, 1)

    def __str__(self) -> str:
        return f"{self.mes:02d}/{self.ano}"

@dataclass(frozen=True)
class PrecoItemCatalogo:
    item: ItemCatalogo
    preco_unitario: Decimal
    estado: Estado
    fonte_precos: FontePrecos
    competencia: Competencia

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
    quantidade: float
    componentes: list[ComponentePrecificado]

    @property
    def custo_unitario(self):
        return sum(
            componente.custo_unitario
            for componente in self.componentes
        )

    @property
    def custo_total(self):
        return self.custo_unitario * self.quantidade
    
@dataclass
class Orcamento:
    id: str
    nome: str
    descricao: str | None
    estado: Estado
    fonte_precos: FontePrecos
    competencia: Competencia
    itens: list[ComposicaoPrecificada]

    @property
    def custo_total(self):
        return sum(item.custo_total for item in self.itens)
