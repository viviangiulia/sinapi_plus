from app.orcamento_service import gerar_orcamento
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

class ComposicoesMock:

    def gerar_orcamento_aleatorio(self):
        catalogo_base = Catalogo(codigo="CATPROPRIO", nome="base_composicoes_v2")

        return [
            ComposicaoQuantificada(
                codigo_composicao="COMP-AGUA-002",
                quantidade=random.randint(1, 25),
                catalogo=catalogo_base
            ),
            ComposicaoQuantificada(
                codigo_composicao="COMP-ESGOTO-003",
                quantidade=random.randint(1, 3),
                catalogo=catalogo_base
            ),
        ]


def test_gerar_orcamento() -> Orcamento:

    

    fonte_precos_base = FontePrecos(
        codigo="BPDEFAULT", nome="precos_composicoes_insumos"
    )

    orcamento = gerar_orcamento(
        nome='Orçamento Teste',
        descricao='Orçamento Mock para Teste Unitário',
        estado=Estado(sigla="MG"),
        fonte_precos=fonte_precos_base,
        competencia=Competencia(
            ano=2025,
            mes=9
        ),
        composicoes_orcamento=ComposicoesMock().gerar_orcamento_aleatorio(),             
    )

    assert orcamento.custo_total > 0
    assert orcamento.id
    assert orcamento.nome
    assert orcamento.competencia
    assert len(orcamento.itens) > 0
