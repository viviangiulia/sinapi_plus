from fastapi.testclient import TestClient
from unittest.mock import patch
from app.api.main import app
from fastapi import HTTPException
from app.api.routers import orcamentos 

client = TestClient(app)


def test_rota_retorna_created():
    payload = {
        "nome": "Orçamento Teste",
        "descricao": None,
        "estado": "MG",
        "fonte_precos": "precos_composicoes_insumos",
        "competencia": "2025-09-01",
        "itens": [],
    }

    response = client.post(
        "/orcamento/orcamentos",
        json=payload,
    )

    assert response.status_code == 201, response.json()


@patch("app.api.routers.orcamentos.executar")
def test_retorna_404_quando_orcamento_nao_encontrado(mock_executar):
    
    mock_executar.side_effect = HTTPException(
        status_code=404,
        detail="Orçamento não encontrado",
    )

    response = client.post("/orcamento/orcamentos", json={
        "nome": "Orçamento Teste",
        "descricao": None,
        "estado": "MG",
        "fonte_precos": "precos_composicoes_insumos",
        "competencia": "2025-09-01",
        "itens": [],
    }) 

    assert response.status_code == 404
    assert response.json()["detail"] == "Orçamento não encontrado"