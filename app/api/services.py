from app.application.mappers import request_to_input_dto
from app.orcamento_service import gerar_orcamento_service,salvar_orcamento_service, consultar_orcamento_service
from app.api.presenters import to_response
from app.api.schemas.requests import GerarOrcamentoRequest
from app.api.schemas.responses import GerarOrcamentoResponse

def executar(dados: GerarOrcamentoRequest) -> GerarOrcamentoResponse:
    orcamento_dto = request_to_input_dto(dados)
    
    # 1. Gerar orçamento
    orcamento = gerar_orcamento_service(orcamento_dto)
    # 2. Salvar orçamento
    salvar_orcamento_service(orcamento)

    # 3. Converter resultado em response
    response = to_response(orcamento)
    return response
 
