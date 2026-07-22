from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal
from datetime import date
from app.api.schemas.requests import FontePrecoschema

class ItemOrcamentoResponse(BaseModel):
    codigo: str = Field(description="Código da composição no catálogo.")

    quantidade: Decimal = Field(
        gt=0,
    )

    categoria: str = Field(
        max_length=100,
    )



class OrcamentoResponse(BaseModel):
    id: UUID

    nome: str = Field(title="Nome do Orçamento", max_length=50)

    custo_total: Decimal = Field(ge=0.0)

    itens: list[ItemOrcamentoResponse] = Field(default_factory=list)


class ConsultarOrcamentoResponse(BaseModel):
    id: UUID

    nome: str = Field(title="Nome do Orçamento", max_length=50)

    custo_total: Decimal = Field(ge=0.0)

    itens: list[ItemOrcamentoResponse] = Field(default_factory=list)

class ResumoOrcamentoResponse(BaseModel):
    id: UUID = Field(title="Identificador do Orçamento")

    nome: str = Field(
        title="Nome do Orçamento",
        max_length=50,
    )

    descricao: str | None = Field(
        default=None,
        title="Descrição do Orçamento",
        max_length=200,
    )

    estado: str = Field(
        title="Estado",
        min_length=2,
        max_length=2,
    )

    fonte_precos: FontePrecoschema = Field(
        title="Fonte de Preços",
    )

    competencia: date = Field(
        title="Competência"
    )

    custo_total: Decimal = Field(
        title="Custo Total",
    )