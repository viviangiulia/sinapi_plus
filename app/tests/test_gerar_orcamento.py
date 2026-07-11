from app.orcamento_service import gerar_orcamento
from app.models import ElementoQuantificavel,Especificacao, Orcamento,Estado
import random

class ElementosFake:

    def gerar_orcamento_aleatorio(self):
        return [
            ElementoQuantificavel(
                categoria="HIDROMETRO",
                quantidade=random.randint(1,25),
                especificacao=Especificacao(
                    diametro=20
                )
            ),
            ElementoQuantificavel(
                categoria="POCO_VISITA",
                quantidade=random.randint(1,3),
                especificacao=Especificacao(
                    diametro=1000,
                    material="CONCRETO",
                    profundidade=1.5
                )
            )
        ]




def test_gerar_orcamento() -> Orcamento:
    
    orcamento = gerar_orcamento(elementos=ElementosFake().gerar_orcamento_aleatorio(),estado=Estado(sigla="MG"))

    assert orcamento.custo_total > 0
    assert orcamento.id
    assert len(orcamento.itens) > 0