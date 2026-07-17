from app.application.mappers import request_to_input_dto
from app.api.schemas.requests import (
    GerarOrcamentoRequest,
    FontePrecoschema,
    ItemOrcamentoRequest,
    CatalogoSchema
)


def test_mapper_converte_request_para_dto():
    request = GerarOrcamentoRequest(
        nome="Residencial Teste",
        estado="RJ",
        fonte_precos=FontePrecoschema.SINAPI,
        competencia="2025-09-01",
        itens=[
            ItemOrcamentoRequest(
                codigo="COMP-AGUA-002",
                catalogo=CatalogoSchema.SINAPI,
                quantidade=4,
                categoria="INSTALAÇÕES HIDROSSANITÁRIAS"
            )
        ],
    )

    dto = request_to_input_dto(request)

    assert dto.nome == request.nome
    assert dto.estado == request.estado
    assert dto.fonte_precos == request.fonte_precos
    assert dto.competencia.ano == 2025
    assert dto.competencia.mes == 9

    assert len(dto.itens) == 1

    item = dto.itens[0]

    assert item.codigo_composicao == "COMP-AGUA-002"
    assert item.quantidade == 4
    assert item.categoria == "INSTALAÇÕES HIDROSSANITÁRIAS"
