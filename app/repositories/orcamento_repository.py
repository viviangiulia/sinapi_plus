from app.infrastructure.database.engine import engine
from app.models import Orcamento
from sqlalchemy.orm import Session
from app.infrastructure.database.orm import OrcamentoOrm
from app.exceptions import OrcamentoNaoEncontradoError

class OrcamentoRepository:

    def __init__(self, session: Session):
        self.session = session

    def salvar_orcamento(self, orcamento: Orcamento) -> None:
        orcamento_orm = OrcamentoOrm(
            id=orcamento.id
        )

        self.session.add(orcamento_orm)

    def buscar_orcamento(self, id: str) -> Orcamento:

        orcamento_orm = self.session.get(OrcamentoOrm, id)

        if orcamento_orm is None:
            raise OrcamentoNaoEncontradoError(
                f"Orçamento {id} não encontrado."
            )

        # TODO: reconstruir os itens quando forem persistidos no ORM.
        return Orcamento(
            id=orcamento_orm.id,
            itens=[]
        )

