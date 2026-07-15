from fastapi import FastAPI
from app.api.routers import orcamentos

app = FastAPI(
    title='SINAPI+ API',
    description='API da aplicação SINAPI+',
    version="0.1.0"
)

app.include_router(orcamentos.orcamento_router)



@app.get("/",status_code=200)
async def home():
    return {
        "name": "SINAPI+ API",
        "version": "0.1.0"
    }

@app.get("/health",status_code=200)
async def health_status():
    return {"message":"Ok"}
