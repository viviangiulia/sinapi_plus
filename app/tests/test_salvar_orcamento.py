import pytest
from app.models import Orcamento
from app.repositories.orcamento_repository import OrcamentoRepository
from app.infrastructure.database.orm import OrcamentoOrm
from unittest.mock import Mock




def test_salvar_orcamento_converte_dominio_em_orm():
    session_mock = Mock()

    repository = OrcamentoRepository(
        session=session_mock
    )

    orcamento = Orcamento(
        id="202607GENERIC",
        itens=[]
    )

    repository.salvar_orcamento(orcamento)

    session_mock.add.assert_called_once()

    objeto_adicionado = session_mock.add.call_args.args[0]

    assert isinstance(objeto_adicionado, OrcamentoOrm)
    assert objeto_adicionado.id == orcamento.id
    
