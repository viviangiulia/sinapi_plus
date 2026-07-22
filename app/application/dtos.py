from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class EstadoInputDTO:
    sigla: str

@dataclass(frozen=True)
class FontePrecosDTO:
    """A base que é utilizada como referência de preços"""
    codigo: str

@dataclass(frozen=True)
class CompetenciaInputDTO:
    ano: int
    mes: int


@dataclass
class ComposicaoQuantificadaInputDTO:
    codigo_composicao: str
    catalogo: str
    quantidade: float
    categoria: str

@dataclass(frozen=True)
class OrcamentoInputDTO:
    nome: str
    descricao: str | None
    estado: str
    fonte_precos: str
    competencia: CompetenciaInputDTO
    itens: list[ComposicaoQuantificadaInputDTO]


@dataclass(frozen=True)
class QueryOrcamentosDTO:
    nome: str | None = None
    descricao: str | None = None
    estado: str | None = None
    fonte_precos: str | None = None

    competencia: date | None = None
    competencia_inicio: date | None = None
    competencia_fim: date | None = None

    page: int = 1
    limit: int = 10