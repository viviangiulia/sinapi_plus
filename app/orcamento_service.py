from app.models import (
    Estado,
    Orcamento,
    ComposicaoPrecificada,
    ComponentePrecificado,
    Catalogo,
    FontePrecos,
    ComposicaoQuantificada,
)
from app.repositories.composicao_repository import ComposicaoRepository
from app.repositories.preco_repository import PrecoRepository
from app.repositories.orcamento_repository import OrcamentoRepository
import uuid
from app.infrastructure.database.engine import engine
from sqlalchemy.orm import Session
from datetime import date


def gerar_orcamento(
    nome: str,
    descricao: str | None,
    estado: Estado,
    fonte_precos: FontePrecos,
    competencia: date,
    composicoes_orcamento: list[ComposicaoQuantificada],
) -> Orcamento:

    composicao_repository = ComposicaoRepository()
    preco_repository = PrecoRepository()

    itens_orcamento = []

    for composicao_quantificada in composicoes_orcamento:

        codigo_composicao = composicao_quantificada.codigo_composicao

        composicao = composicao_repository.buscar_composicao(
            codigo_composicao, composicao_quantificada.catalogo
        )

        lista_componentes = []

        for componente in composicao.items:

            preco_item = preco_repository.buscar_preco(
                item=componente.item,
                estado=estado,
                fonte_precos=fonte_precos,
                competencia=competencia,
            )

            componente_precificado = ComponentePrecificado(
                componente=componente, preco_unitario=preco_item.preco_unitario
            )

            lista_componentes.append(componente_precificado)

        composicao_precificada = ComposicaoPrecificada(
            codigo=codigo_composicao,
            descricao=composicao.descricao,
            quantidade=composicao_quantificada.quantidade,
            componentes=lista_componentes,
            categoria=composicao_quantificada.categoria,
            unidade=composicao.unidade
        )

        itens_orcamento.append(composicao_precificada)

    return Orcamento(
        id=str(uuid.uuid4()),
        nome=nome,
        descricao=descricao,
        estado=estado,
        fonte_precos=fonte_precos,        
        competencia=competencia,
        itens=itens_orcamento,
    )


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
