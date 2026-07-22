from pydantic import BaseModel, Field, model_validator
from decimal import Decimal
from datetime import date
from enum import Enum


class CatalogoSchema(str, Enum):
    SINAPI = "base_composicoes_v2"


class FontePrecoschema(str, Enum):
    SINAPI = "precos_composicoes_insumos"


class ItemOrcamentoRequest(BaseModel):
    codigo: str = Field(description="Código da composição no catálogo.")

    catalogo: CatalogoSchema = Field(
        description="Catálogo onde a composição será pesquisada.",
        default=CatalogoSchema.SINAPI,
    )

    quantidade: Decimal = Field(
        gt=0,
    )

    categoria: str = Field(
        max_length=100,
    )


class GerarOrcamentoRequest(BaseModel):

    nome: str = Field(title="Nome do Orçamento", max_length=50)

    descricao: str | None = Field(
        default=None, title="Descrição do Orçamento", max_length=200
    )

    estado: str = Field(
        title="Estado",
        description="Estado Utilizado como referência para consulta de preços da SINAPI.",
        max_length=2,
        min_length=2,
    )

    fonte_precos: FontePrecoschema = Field(
        description="Base de Preços Utilizada por padrão é SINAPI.",
        max_length=50,
        default=FontePrecoschema.SINAPI,
    )

    competencia: date

    itens: list[ItemOrcamentoRequest] = Field(default_factory=list)


class QueryOrcamentosRequest(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    estado: str | None = Field(default=None, max_length=2, min_length=2)
    fonte_precos: FontePrecoschema = Field(
        max_length=50,
        default=FontePrecoschema.SINAPI,
    )

    competencia: date | None = None
    competencia_inicio: date | None = None
    competencia_fim: date | None = None

    page: int = Field(ge=1, default=1)
    limit: int = Field(ge=1, le=100, default=10)

    @model_validator(mode="after")
    def validar_intervalo_datas(self):
        if (
            self.competencia_inicio
            and self.competencia_fim
            and self.competencia_inicio > self.competencia_fim
        ):
            raise ValueError(
                "competencia_inicio deve ser anterior ou igual a competencia_fim."
            )

        return self
