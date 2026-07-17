from app.api.schemas.requests import GerarOrcamentoRequest
from app.application.dtos import (
    OrcamentoInputDTO,
    CompetenciaInputDTO,
    ComposicaoQuantificadaInputDTO,
)


def request_to_input_dto(payload: GerarOrcamentoRequest) -> OrcamentoInputDTO:

    nome = payload.nome
    descricao = payload.descricao
    estado = payload.estado
    fonte_precos = payload.fonte_precos.value
    competencia = CompetenciaInputDTO(
        ano=payload.competencia.year, mes=payload.competencia.month
    )

    itens = []

    for item_request in payload.itens:
        itens.append(
            ComposicaoQuantificadaInputDTO(
                codigo_composicao=item_request.codigo, catalogo=item_request.catalogo.value
            ,
            quantidade=float(item_request.quantidade),
            categoria=item_request.categoria,
        ))

    return OrcamentoInputDTO(
        nome=nome,
        descricao=descricao,
        estado=estado,
        fonte_precos=fonte_precos,
        competencia=competencia,
        itens=itens,
    )
