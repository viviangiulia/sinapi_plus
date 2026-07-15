from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal

class ItemOrcamentoResponse(BaseModel):
    codigo: str = Field(description="Código da composição no catálogo.")

    quantidade: Decimal = Field(
        gt=0,
    )

    categoria: str = Field(
        max_length=100,
    )



class GerarOrcamentoResponse(BaseModel):
    id: UUID

    nome: str = Field(title="Nome do Orçamento", max_length=50)

    custo_total: Decimal = Field(ge=0.0)

    itens: list[ItemOrcamentoResponse] = Field(default_factory=list)