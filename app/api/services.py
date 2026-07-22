from app.application.mappers import request_to_input_dto, request_query_to_dto
from app.orcamento_service import gerar_orcamento_service,salvar_orcamento_service, consultar_orcamento_service,listar_orcamento_service
from app.api.presenters import to_response, to_resumo_response
from app.api.schemas.requests import GerarOrcamentoRequest, QueryOrcamentosRequest
from app.api.schemas.responses import OrcamentoResponse, ResumoOrcamentoResponse
from uuid import UUID
from typing import List

def gerar_orcamento_use_case(dados: GerarOrcamentoRequest) -> OrcamentoResponse:
    orcamento_dto = request_to_input_dto(dados)
    
    # 1. Gerar orçamento
    orcamento = gerar_orcamento_service(orcamento_dto)
    # 2. Salvar orçamento
    salvar_orcamento_service(orcamento)

    # 3. Converter resultado em response
    response = to_response(orcamento)
    return response
 

def consultar_orcamento_use_case(id: UUID) -> OrcamentoResponse:

    resultado = consultar_orcamento_service(id)

    response = to_response(resultado)

    return response
    

def listar_orcamento_use_case(request_data:QueryOrcamentosRequest) -> List[ResumoOrcamentoResponse]:

    dados = request_query_to_dto(request_data)
    
    resultados = listar_orcamento_service(dados)

    return [to_resumo_response(orcamento) for orcamento in resultados]