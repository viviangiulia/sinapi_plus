from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Date,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class OrcamentoOrm(Base):
    __tablename__ = "orcamentos"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    descricao: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    estado: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )

    fonte_precos: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    competencia: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    itens: Mapped[list["ComposicaoPrecificadaOrm"]] = relationship(
        back_populates="orcamento",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"OrcamentoOrm(id={self.id!r}, nome={self.nome!r})"


class ComposicaoPrecificadaOrm(Base):
    __tablename__ = "composicoes_precificadas"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    orcamento_id: Mapped[str] = mapped_column(
        ForeignKey("orcamentos.id"),
        nullable=False,
    )

    codigo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    descricao: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    unidade: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    categoria: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    quantidade: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
    )

    custo_unitario: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        nullable=False,
    )

    custo_total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    orcamento: Mapped["OrcamentoOrm"] = relationship(
        back_populates="itens",
    )

    componentes: Mapped[
        list["ComponenteComposicaoPersistidoOrm"]
    ] = relationship(
        back_populates="composicao_precificada",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"ComposicaoPrecificadaOrm("
            f"id={self.id!r}, "
            f"codigo={self.codigo!r}, "
            f"categoria={self.categoria!r}"
            f")"
        )


class ComponenteComposicaoPersistidoOrm(Base):
    __tablename__ = "componentes_composicao_persistidos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    composicao_precificada_id: Mapped[int] = mapped_column(
        ForeignKey("composicoes_precificadas.id"),
        nullable=False,
    )

    codigo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    descricao: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    unidade: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    coeficiente: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False,
    )

    custo_unitario: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        nullable=False,
    )

    catalogo: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    composicao_precificada: Mapped["ComposicaoPrecificadaOrm"] = relationship(
        back_populates="componentes",
    )

    def __repr__(self) -> str:
        return (
            f"ComponenteComposicaoPersistidoOrm("
            f"id={self.id!r}, "
            f"codigo={self.codigo!r}"
            f")"
        )