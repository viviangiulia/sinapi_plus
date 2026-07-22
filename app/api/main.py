from fastapi import FastAPI
from app.api.routers import orcamentos
from fastapi.responses import JSONResponse
from app.exceptions import OrcamentoNaoEncontradoError


app = FastAPI(
    title='SINAPI+ API',
    description='API da aplicação SINAPI+',
    version="0.1.0"
)

app.include_router(orcamentos.orcamento_router)


@app.exception_handler(OrcamentoNaoEncontradoError)
async def handle_orcamento_nao_encontrado(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        },
    )


@app.get("/",status_code=200)
async def home():
    return {
        "name": "SINAPI+ API",
        "version": "0.1.0"
    }

@app.get("/health",status_code=200)
async def health_status():
    return {"message":"Ok"}
