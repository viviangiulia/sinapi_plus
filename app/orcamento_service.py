from app.models import (
    Estado,
    Orcamento,
    ComposicaoPrecificada,
    ComponentePrecificado,
    FontePrecos,
    Competencia,
    Catalogo
)
from app.repositories.composicao_repository import ComposicaoRepository
from app.repositories.preco_repository import PrecoRepository
from app.repositories.orcamento_repository import OrcamentoRepository
import uuid
from uuid import UUID
from app.infrastructure.database.engine import engine
from sqlalchemy.orm import Session
from app.application.dtos import OrcamentoInputDTO, QueryOrcamentosDTO


def gerar_orcamento_service(
    dto: OrcamentoInputDTO,
) -> Orcamento:
    nome = dto.nome
    descricao = dto.descricao
    composicoes_orcamento = dto.itens
    estado = Estado(sigla=dto.estado)
    fonte_precos = FontePrecos(codigo=dto.fonte_precos)
    competencia = Competencia(
        ano=dto.competencia.ano,
        mes=dto.competencia.mes)

    composicao_repository = ComposicaoRepository()
    preco_repository = PrecoRepository()

    itens_orcamento = []

    for composicao_quantificada in composicoes_orcamento:

        codigo_composicao = composicao_quantificada.codigo_composicao

        composicao = composicao_repository.buscar_composicao(
            codigo_composicao, Catalogo(codigo=composicao_quantificada.catalogo)
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
            unidade=composicao.unidade,
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


def salvar_orcamento_service(orcamento: Orcamento) -> None:

    with Session(engine) as session:

        repository = OrcamentoRepository(session)

        try:
            repository.salvar_orcamento(orcamento)
            session.commit()
            print("Orçamento salvo com sucesso!")

        except Exception:
            session.rollback()
            raise


def consultar_orcamento_service(id: UUID) -> Orcamento:
    with Session(engine) as session:
        repository = OrcamentoRepository(session)

        return repository.buscar_orcamento(id)


def listar_orcamento_service(dados:QueryOrcamentosDTO):
    with Session(engine) as session:
        repository = OrcamentoRepository(session)

        return repository.listar_orcamentos(dados)