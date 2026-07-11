from app.models import (
    ElementoQuantificavel,
    Estado,
    Orcamento,
    ComposicaoPrecificada,
    ComponentePrecificado,
)
from app.repositories.composicao_repository import ComposicaoRepository
from app.repositories.preco_repository import PrecoRepository
from app.repositories.catalogo_repository import CatalogoRepository
from app.repositories.orcamento_repository import OrcamentoRepository
import uuid
from app.infrastructure.database.engine import engine
from sqlalchemy.orm import Session


def gerar_orcamento(
    elementos: list[ElementoQuantificavel], estado: Estado
) -> Orcamento:

    catalogo_repository = CatalogoRepository()
    composicao_repository = ComposicaoRepository()
    preco_repository = PrecoRepository()

    itens_orcamento = []

    for elemento in elementos:
        composicao_quantificada = catalogo_repository.buscar_codigo_composicao(elemento)

        codigo_composicao = composicao_quantificada.codigo_composicao

        composicao = composicao_repository.buscar_composicao(codigo_composicao)

        lista_componentes = []

        for componente in composicao.items:
            preco_item = preco_repository.buscar_preco(
                item=componente.item,
                estado=estado,
            )

            componente_precificado = ComponentePrecificado(
                componente=componente, preco_unitario=preco_item.preco_unitario
            )

            lista_componentes.append(componente_precificado)

        composicao_precificada = ComposicaoPrecificada(
            codigo=codigo_composicao,
            estado=estado,
            quantidade=elemento.quantidade,
            componentes=lista_componentes,
        )

        itens_orcamento.append(composicao_precificada)

    return Orcamento(id=str(uuid.uuid4()), itens=itens_orcamento)


def salvar_orcamento(orcamento: Orcamento) -> None:

    with Session(engine) as session:

        repository = OrcamentoRepository(session)

        try:
            repository.salvar_orcamento(orcamento)
            session.commit()
            print("Orçamento salvo com sucesso!")

        except Exception:
            session.rollback()
            raise


def consultar_orcamento_salvo(id: str) -> Orcamento:
    with Session(engine) as session:
        repository = OrcamentoRepository(session)

        return repository.buscar_orcamento(id)
