from app.models import Orcamento
from app.api.schemas.responses import GerarOrcamentoResponse,ItemOrcamentoResponse

def to_response(dados:Orcamento) -> GerarOrcamentoResponse:

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

    return GerarOrcamentoResponse(
        id=id,
        nome=nome,
        custo_total=custo_total,
        itens=itens
    )