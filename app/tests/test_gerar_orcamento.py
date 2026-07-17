from app.orcamento_service import gerar_orcamento_service
from app.models import (
    Competencia,
    Orcamento,
    Estado,
    Catalogo,
    FontePrecos,
    ComposicaoQuantificada,
)
import random
from datetime import date
from app.application.dtos import (
    OrcamentoInputDTO,
    CompetenciaInputDTO,
    ComposicaoQuantificadaInputDTO,
)


class ComposicoesMock:

    def gerar_orcamento_aleatorio(self):
        catalogo_base = Catalogo(codigo="base_composicoes_v2")

        return [
            ComposicaoQuantificada(
                codigo_composicao="COMP-AGUA-002",
                quantidade=random.randint(1, 25),
                catalogo=catalogo_base,
                categoria="Água Potável",
            ),
            ComposicaoQuantificada(
                codigo_composicao="COMP-ESGOTO-003",
                quantidade=random.randint(1, 3),
                catalogo=catalogo_base,
                categoria="Esgoto Sanitário",
            ),
        ]


def test_gerar_orcamento() -> Orcamento:

    fonte_precos_base = "precos_composicoes_insumos"

    dados = OrcamentoInputDTO(
        nome="Orçamento Teste",
        descricao="Orçamento Mock para Teste Unitário",
        estado="MG",
        fonte_precos=fonte_precos_base,
        competencia=CompetenciaInputDTO(ano=2025, mes=9),
        itens=[
            ComposicaoQuantificadaInputDTO(
                codigo_composicao="COMP-AGUA-001",
                catalogo="base_composicoes_v2",
                quantidade=45.8,
                categoria="INSTALAÇÕES HIDROSSANITÁRIAS",
            )
        ],
    )

    orcamento = gerar_orcamento_service(dados)

    assert orcamento.custo_total > 0
    assert orcamento.id
    assert orcamento.nome
    assert orcamento.competencia
    assert len(orcamento.itens) > 0
