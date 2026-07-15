from fastapi import APIRouter
from app.api.schemas.requests import GerarOrcamentoRequest
from app.api.schemas.responses import GerarOrcamentoResponse

orcamento_router = APIRouter(prefix="/orcamento",tags=["ORÇAMENTO"])


@orcamento_router.post("/orcamentos",response_model=GerarOrcamentoResponse,status_code=201)
async def gerar_orcamento(dados: GerarOrcamentoRequest):
    # TODO desenvolver e chamar o serviço que converte os dados da API
    # Em dados do domínio, chamar a pipeline de cálculo e depois converter
    # o resultado na resposta tudo com tratamento de erros
    pass
