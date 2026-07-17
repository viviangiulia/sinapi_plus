from fastapi import APIRouter, HTTPException
from app.api.schemas.requests import GerarOrcamentoRequest
from app.api.schemas.responses import GerarOrcamentoResponse
from app.api.services import executar

orcamento_router = APIRouter(prefix="/orcamento",tags=["ORÇAMENTO"])


@orcamento_router.post("/orcamentos",response_model=GerarOrcamentoResponse,status_code=201)
async def gerar_orcamento(dados: GerarOrcamentoRequest):
    try:
        response = executar(dados)
        return response
    except HTTPException:
        raise 
     
    

