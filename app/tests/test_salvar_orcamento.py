import pytest
from app.models import (
    Orcamento,
    Competencia,
    ComposicaoPrecificada,
    FontePrecos,
    ComponentePrecificado,
    ComponenteComposicao,
    ItemCatalogo,
    TipoItem,
    Catalogo,
    Estado
)
from app.repositories.orcamento_repository import OrcamentoRepository
from app.infrastructure.database.orm import (
    OrcamentoOrm,
    ComposicaoPrecificadaOrm,
    ComponenteComposicaoPersistidoOrm,
)
from unittest.mock import Mock
from sqlalchemy import select
from datetime import date
from decimal import Decimal


def test_salvar_orcamento_converte_dominio_em_orm():
    session_mock = Mock()

    repository = OrcamentoRepository(session=session_mock)

    orcamento = Orcamento(
        id="202607GENERIC",
        nome="Orçamento Teste",
        descricao="Orçamento para teste de persistência",
        estado=Estado(sigla="SP"),
        fonte_precos=Mock(),
        competencia=Competencia(2025, 9),
        itens=[],
    )

    repository.salvar_orcamento(orcamento)

    session_mock.add.assert_called_once()

    objeto_adicionado = session_mock.add.call_args.args[0]

    assert isinstance(objeto_adicionado, OrcamentoOrm)
    assert objeto_adicionado.id == orcamento.id


def test_composicao_referencia_orcamento_ao_ser_adicionada_aos_itens():
    orcamento_orm = OrcamentoOrm(
        id="202607GENERIC",
        nome="Orçamento Teste",
        descricao=None,
        estado="SP",
        fonte_precos="SINAPI",
        competencia=date(2025, 9, 1),
    )

    composicao_orm = ComposicaoPrecificadaOrm(
        codigo="12345",
        descricao="Composição teste",
        unidade="M2",
        categoria="Estrutura",
        quantidade=Decimal("10"),
        custo_unitario=Decimal("100"),
        custo_total=Decimal("1000"),
    )

    orcamento_orm.itens.append(composicao_orm)

    assert composicao_orm.orcamento is orcamento_orm


# def test_componente_referencia_composicao_ao_ser_adicionado():
#     composicao_orm = criar_composicao_orm()

#     componente_orm = ComponenteComposicaoPersistidoOrm(
#         codigo="00001",
#         descricao="Aço CA-50",
#         tipo="MATERIAL",
#         unidade="KG",
#         coeficiente=Decimal("10.5"),
#         custo_unitario=Decimal("8.75"),
#     )

#     composicao_orm.componentes.append(componente_orm)

#     assert componente_orm.composicao_precificada is composicao_orm

# def test_salvar_orcamento_persiste_composicoes_associadas(session):
#     orcamento = criar_orcamento_com_composicoes()

#     repository = OrcamentoRepository(session=session)

#     repository.salvar_orcamento(orcamento)
#     session.flush()

#     composicoes = session.scalars(
#         select(ComposicaoPrecificadaOrm).where(
#             ComposicaoPrecificadaOrm.orcamento_id == orcamento.id
#         )
#     ).all()

#     assert len(composicoes) == len(orcamento.itens)

#     assert composicoes[0].orcamento_id == orcamento.id
#     assert composicoes[0].codigo == orcamento.itens[0].codigo


def test_salvar_orcamento_persiste_componentes_da_composicao(session):

    repository = OrcamentoRepository(session=session)

    orcamento = criar_orcamento_com_composicao_e_componentes()

    repository.salvar_orcamento(orcamento)
    session.flush()

    composicao = session.scalars(
        select(ComposicaoPrecificadaOrm).where(
            ComposicaoPrecificadaOrm.orcamento_id == orcamento.id
        )
    ).one()

    componentes = session.scalars(
        select(ComponenteComposicaoPersistidoOrm).where(
            ComponenteComposicaoPersistidoOrm.composicao_precificada_id == composicao.id
        )
    ).all()

    assert len(componentes) == 1

    assert componentes[0].codigo == "95673"
    assert componentes[0].coeficiente == Decimal("1")
    assert componentes[0].custo_unitario == Decimal("45")


def criar_orcamento_com_composicao_e_componentes() -> Orcamento:
    return Orcamento(
        id="202607GENERIC",
        nome="Orçamento Teste",
        descricao="Orçamento para teste de persistência",
        estado=Estado(sigla="SP"),
        fonte_precos=FontePrecos(
            codigo="precos_composicoes_insumos",
        ),
        competencia=Competencia(2025, 9),
        itens=[
            ComposicaoPrecificada(
                codigo="COMP-AGUA-002",
                descricao=(
                    "Instalação de hidrômetro DN 20 com capacidade "
                    "1,5 m³/h - fornecimento e montagem"
                ),
                categoria="INSTALAÇÕES HIDROSSANITÁRIAS",
                quantidade=4,
                unidade="UN",
                componentes=[
                    ComponentePrecificado(
                        componente=ComponenteComposicao(
                            item=ItemCatalogo(
                                codigo="95673",
                                descricao=(
                                    "HIDRÔMETRO DN 20 (½?), 1,5 M³/H ? "
                                    "FORNECIMENTO E INSTALAÇÃO. AF_11/2016"
                                ),
                                tipo=TipoItem.COMPOSICAO,
                                catalogo=Catalogo(
                                    codigo="base_composicoes_v2"
                                ),
                                unidade="M3",
                            ),
                            coeficiente=1,
                        ),
                        preco_unitario=45,
                    )
                ],
            )
        ],
    )


def test_orcamento_recuperado_preserva_resultados_originais(session):
    repository = OrcamentoRepository(session)

    original = criar_orcamento_com_composicao_e_componentes()

    repository.salvar_orcamento(original)
    session.flush()

    recuperado = repository.buscar_orcamento(original.id)

    assert recuperado.custo_total == original.custo_total
    assert recuperado.itens[0].custo_unitario == original.itens[0].custo_unitario
    assert recuperado.itens[0].custo_total == original.itens[0].custo_total


def test_salvar_orcamento_persiste_composicao_associada(session):
    repository = OrcamentoRepository(session=session)
    orcamento = criar_orcamento_com_composicao_e_componentes()

    repository.salvar_orcamento(orcamento)
    session.flush()

    composicoes = session.scalars(
        select(ComposicaoPrecificadaOrm).where(
            ComposicaoPrecificadaOrm.orcamento_id == orcamento.id
        )
    ).all()

    assert len(composicoes) == 1

    composicao = composicoes[0]

    assert composicao.orcamento_id == orcamento.id
    assert composicao.codigo == "COMP-AGUA-002"
    assert composicao.descricao == (
        "Instalação de hidrômetro DN 20 com capacidade "
        "1,5 m³/h - fornecimento e montagem"
    )
    assert composicao.unidade == "UN"
    assert composicao.categoria == "INSTALAÇÕES HIDROSSANITÁRIAS"
    assert composicao.quantidade == Decimal("4.000000")
    assert composicao.custo_unitario == Decimal("45.0000")
    assert composicao.custo_total == Decimal("180.00")


def test_salvar_orcamento_persiste_componentes_da_composicao(session):
    repository = OrcamentoRepository(session=session)
    orcamento = criar_orcamento_com_composicao_e_componentes()

    repository.salvar_orcamento(orcamento)
    session.flush()

    composicao = session.scalars(
        select(ComposicaoPrecificadaOrm).where(
            ComposicaoPrecificadaOrm.orcamento_id == orcamento.id
        )
    ).one()

    componentes = session.scalars(
        select(ComponenteComposicaoPersistidoOrm).where(
            ComponenteComposicaoPersistidoOrm.composicao_precificada_id
            == composicao.id
        )
    ).all()

    assert len(componentes) == 1

    componente = componentes[0]

    assert componente.composicao_precificada_id == composicao.id
    assert componente.codigo == "95673"
    assert componente.descricao == (
        "HIDRÔMETRO DN 20 (½?), 1,5 M³/H ? "
        "FORNECIMENTO E INSTALAÇÃO. AF_11/2016"
    )
    assert componente.unidade == "M3"
    assert componente.tipo == TipoItem.COMPOSICAO.value
    assert componente.catalogo == "base_composicoes_v2"
    assert componente.coeficiente == Decimal("1.00000000")
    assert componente.custo_unitario == Decimal("45.0000")

def test_orcamento_recuperado_preserva_dados_e_resultados_originais(
    session,
):
    repository = OrcamentoRepository(session=session)

    original = criar_orcamento_com_composicao_e_componentes()

    repository.salvar_orcamento(original)
    session.flush()

    recuperado = repository.buscar_orcamento(original.id)

    assert recuperado.id == original.id
    assert recuperado.nome == original.nome
    assert recuperado.descricao == original.descricao
    assert recuperado.estado == original.estado
    assert recuperado.fonte_precos == original.fonte_precos
    assert recuperado.competencia == original.competencia
    assert recuperado.custo_total == original.custo_total

    assert len(recuperado.itens) == len(original.itens)

    composicao_original = original.itens[0]
    composicao_recuperada = recuperado.itens[0]

    assert composicao_recuperada.codigo == composicao_original.codigo
    assert composicao_recuperada.descricao == composicao_original.descricao
    assert composicao_recuperada.unidade == composicao_original.unidade
    assert composicao_recuperada.categoria == composicao_original.categoria
    assert composicao_recuperada.quantidade == composicao_original.quantidade
    assert (
        composicao_recuperada.custo_unitario
        == composicao_original.custo_unitario
    )
    assert (
        composicao_recuperada.custo_total
        == composicao_original.custo_total
    )

    assert len(composicao_recuperada.componentes) == len(
        composicao_original.componentes
    )

    componente_original = composicao_original.componentes[0]
    componente_recuperado = composicao_recuperada.componentes[0]

    assert (
        componente_recuperado.componente.item.codigo
        == componente_original.componente.item.codigo
    )
    assert (
        componente_recuperado.componente.item.descricao
        == componente_original.componente.item.descricao
    )
    assert (
        componente_recuperado.componente.item.unidade
        == componente_original.componente.item.unidade
    )
    assert (
        componente_recuperado.componente.item.tipo
        == componente_original.componente.item.tipo
    )
    assert (
        componente_recuperado.componente.item.catalogo
        == componente_original.componente.item.catalogo
    )
    assert (
        componente_recuperado.componente.coeficiente
        == componente_original.componente.coeficiente
    )
    assert (
        componente_recuperado.preco_unitario
        == componente_original.preco_unitario
    )


def test_permite_mesmo_codigo_de_composicao_em_categorias_diferentes(
    session,
):
    repository = OrcamentoRepository(session=session)

    orcamento = criar_orcamento_com_composicao_e_componentes()

    composicao_original = orcamento.itens[0]

    segunda_composicao = ComposicaoPrecificada(
        codigo=composicao_original.codigo,
        descricao=composicao_original.descricao,
        unidade=composicao_original.unidade,
        quantidade=10,
        categoria="Ligação predial",
        componentes=composicao_original.componentes,
    )

    orcamento.itens.append(segunda_composicao)

    repository.salvar_orcamento(orcamento)
    session.flush()

    composicoes = session.scalars(
        select(ComposicaoPrecificadaOrm).where(
            ComposicaoPrecificadaOrm.orcamento_id
            == orcamento.id
        )
    ).all()

    assert len(composicoes) == 2

    assert {
        composicao.categoria
        for composicao in composicoes
    } == {
    "INSTALAÇÕES HIDROSSANITÁRIAS",
    "Ligação predial",
}

    assert all(
        composicao.codigo == "COMP-AGUA-002"
        for composicao in composicoes
    )