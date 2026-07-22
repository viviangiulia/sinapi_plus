from app.models import Orcamento
from app.api.schemas.responses import OrcamentoResponse,ItemOrcamentoResponse,ResumoOrcamentoResponse
from app.api.schemas.requests import FontePrecoschema
from datetime import date

def to_response(dados:Orcamento) -> OrcamentoResponse:

    id = dados.id
    nome = dados.nome
    custo_total = dados.custo_total

    itens = []

    for item_orcamento in dados.itens:
        itens.append(
            ItemOrcamentoResponse(
                codigo=item_orcamento.codigo,
                quantidade=item_orcamento.quantidade,
                categoria=item_orcamento.categoria
            )
        )

    return OrcamentoResponse(
        id=id,
        nome=nome,
        custo_total=custo_total,
        itens=itens
    )

def to_resumo_response(
    orcamento: Orcamento,
) -> ResumoOrcamentoResponse:
    return ResumoOrcamentoResponse(
        id=orcamento.id,
        nome=orcamento.nome,
        descricao=orcamento.descricao,
        estado=orcamento.estado.sigla,
        fonte_precos=FontePrecoschema(
            orcamento.fonte_precos.codigo
        ),
        competencia=date(
            year=orcamento.competencia.ano,
            month=orcamento.competencia.mes,
            day=1
            ),
        custo_total=orcamento.custo_total,
    )