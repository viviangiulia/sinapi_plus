from fastapi import APIRouter, HTTPException, Query
from app.api.schemas.requests import GerarOrcamentoRequest,QueryOrcamentosRequest
from app.api.schemas.responses import OrcamentoResponse, ResumoOrcamentoResponse
from app.api.services import gerar_orcamento_use_case, consultar_orcamento_use_case,listar_orcamento_use_case
from uuid import UUID
from typing import Annotated

orcamento_router = APIRouter(prefix="/orcamento",tags=["ORÇAMENTO"])


@orcamento_router.post("/orcamentos",response_model=OrcamentoResponse,status_code=201)
async def gerar_orcamento(dados: GerarOrcamentoRequest):
    """Gera um orçamento com base nos dados enviados."""
    try:
        response = gerar_orcamento_use_case(dados)
        return response
    except HTTPException:
        raise 
     
    
@orcamento_router.get("/orcamentos/{id}",response_model=OrcamentoResponse,status_code=200)
async def consultar_orcamento(id:UUID):
    """Consulta um orçamento no banco através do seu ID"""      

    return consultar_orcamento_use_case(id)


@orcamento_router.get(
    "/orcamentos",
    response_model=list[ResumoOrcamentoResponse],
)
async def listar_orcamentos(
    filtros: Annotated[QueryOrcamentosRequest, Query()]
):
    """Busca uma lista de orçamentos com base nos filtros definidos."""
    return listar_orcamento_use_case(filtros)