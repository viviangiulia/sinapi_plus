from app.infrastructure.database.engine import engine
from app.models import Orcamento, ComposicaoPrecificada, ComponentePrecificado,Estado,FontePrecos,Competencia, ComponenteComposicao, TipoItem,ItemCatalogo,Catalogo
from sqlalchemy.orm import Session
from app.infrastructure.database.orm import (
    OrcamentoOrm,
    ComposicaoPrecificadaOrm,
    ComponenteComposicaoPersistidoOrm,
)
from app.exceptions import OrcamentoNaoEncontradoError
from datetime import date


class OrcamentoRepository:

    def __init__(self, session: Session):
        self.session = session

    def salvar_orcamento(self, orcamento: Orcamento) -> None:
        orcamento_orm = OrcamentoOrm(
            id=orcamento.id,
            nome=orcamento.nome,
            descricao=orcamento.descricao,
            estado=orcamento.estado.sigla,
            fonte_precos=orcamento.fonte_precos.codigo,
            competencia=date(
                orcamento.competencia.ano,
                orcamento.competencia.mes,
                1,
            ),
            itens=[
                self._composicao_para_orm(composicao) for composicao in orcamento.itens
            ],
        )

        self.session.add(orcamento_orm)

    def buscar_orcamento(self, id: str) -> Orcamento:
        orcamento_orm = self.session.get(OrcamentoOrm, id)

        if orcamento_orm is None:
            raise OrcamentoNaoEncontradoError(
                f"Orçamento {id} não encontrado."
            )

        return self._orcamento_para_dominio(orcamento_orm)
    
    @classmethod
    def _orcamento_para_dominio(
        cls,
        orcamento_orm: OrcamentoOrm,
    ) -> Orcamento:
        return Orcamento(
            id=orcamento_orm.id,
            nome=orcamento_orm.nome,
            descricao=orcamento_orm.descricao,
            estado=Estado(
                sigla=orcamento_orm.estado,
            ),
            fonte_precos=FontePrecos(
                codigo=orcamento_orm.fonte_precos,
            ),
            competencia=Competencia(
                ano=orcamento_orm.competencia.year,
                mes=orcamento_orm.competencia.month,
            ),
            itens=[
                cls._composicao_para_dominio(composicao_orm)
                for composicao_orm in orcamento_orm.itens
            ],
        )
    
    @classmethod
    def _composicao_para_dominio(
        cls,
        composicao_orm: ComposicaoPrecificadaOrm,
    ) -> ComposicaoPrecificada:
        return ComposicaoPrecificada(
            codigo=composicao_orm.codigo,
            descricao=composicao_orm.descricao,
            unidade=composicao_orm.unidade,
            quantidade=float(composicao_orm.quantidade),
            categoria=composicao_orm.categoria,
            componentes=[
                cls._componente_para_dominio(componente_orm)
                for componente_orm in composicao_orm.componentes
            ],
        )
    
    @staticmethod
    def _componente_para_dominio(
        componente_orm: ComponenteComposicaoPersistidoOrm,
    ) -> ComponentePrecificado:
        item = ItemCatalogo(
            codigo=componente_orm.codigo,
            descricao=componente_orm.descricao,
            unidade=componente_orm.unidade,
            tipo=TipoItem(componente_orm.tipo),
            catalogo=Catalogo(
                codigo=componente_orm.catalogo,
            ),
        )

        componente = ComponenteComposicao(
            item=item,
            coeficiente=float(componente_orm.coeficiente),
        )

        return ComponentePrecificado(
            componente=componente,
            preco_unitario=float(componente_orm.custo_unitario),
        )

    def _composicao_para_orm(
        self,
        composicao: ComposicaoPrecificada,
    ) -> ComposicaoPrecificadaOrm:
        return ComposicaoPrecificadaOrm(
            codigo=composicao.codigo,
            descricao=composicao.descricao,
            quantidade=composicao.quantidade,
            componentes=[
                self._componente_para_orm(componente)
                for componente in composicao.componentes
            ],
            unidade=composicao.unidade,
            categoria=composicao.categoria,
            custo_unitario=composicao.custo_unitario,
            custo_total=composicao.custo_total
        )

    @staticmethod
    def _componente_para_orm(
        componente: ComponentePrecificado,
    ) -> ComponenteComposicaoPersistidoOrm:
        return ComponenteComposicaoPersistidoOrm(
            codigo=componente.componente.item.codigo,
            descricao=componente.componente.item.descricao,
            tipo=componente.componente.item.tipo.value,
            coeficiente=componente.componente.coeficiente,
            custo_unitario=componente.preco_unitario,
            unidade=componente.componente.item.unidade,
            catalogo=componente.componente.item.catalogo.codigo
        )
