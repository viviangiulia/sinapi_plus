from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class OrcamentoOrm(Base):
    __tablename__ = 'orcamentos'

    id: Mapped[str] = mapped_column(String(36),primary_key=True)


    def __repr__(self):
        return f"Orçamento ID: {self.id}"