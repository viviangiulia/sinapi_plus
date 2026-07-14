from dataclasses import dataclass
from decimal import Decimal
from typing import Dict

import pytest

from app.models import (
    Catalogo,
    Competencia,
    Estado,
    FontePrecos,
    ItemCatalogo,
    PrecoItemCatalogo,
    TipoItem,
)


@dataclass
class CatalogoFakePrecos:
    catalogo: Dict

    def buscar_preco(
        self,
        item: ItemCatalogo,
        estado: Estado,
        fonte_precos: FontePrecos,
        competencia: Competencia,
    ) -> PrecoItemCatalogo:

        codigo_item = item.codigo
        preco_unitario = self.catalogo[estado.sigla][codigo_item]

        return PrecoItemCatalogo(
            item=item,
            estado=estado,
            preco_unitario=Decimal(str(preco_unitario)),
            fonte_precos=fonte_precos,
            competencia=competencia,
        )


def test_buscar_preco_item():
    catalogo_precos = CatalogoFakePrecos(
        {
            "MG": {
                "INS-001": 15.00,
                "INS-002": 42.50,
                "INS-003": 8.75,
                "COMP-123": 120.00,
            },
            "SP": {
                "INS-001": 18.20,
                "INS-002": 45.10,
                "INS-003": 9.30,
                "COMP-123": 135.00,
            },
        }
    )

    catalogo = Catalogo(
        codigo="SINAPI",
    )

    fonte_precos = FontePrecos(
        codigo="SINAPI",
    )

    competencia = Competencia(
        ano=2026,
        mes=6,
    )

    estado = Estado(sigla="SP")

    item = ItemCatalogo(
        codigo="INS-001",
        descricao="Areia Média Lavada",
        tipo=TipoItem.INSUMO,
        catalogo=catalogo,
        unidade="M3"
    )

    preco_item = catalogo_precos.buscar_preco(
        item=item,
        estado=estado,
        fonte_precos=fonte_precos,
        competencia=competencia,
    )

    assert preco_item.preco_unitario == Decimal("18.20")
    assert preco_item.estado == estado
    assert preco_item.fonte_precos == fonte_precos
    assert preco_item.competencia == competencia


def test_preco_deve_ser_positivo():
    catalogo = Catalogo(
        codigo="SINAPI",
    )

    fonte_precos = FontePrecos(
        codigo="SINAPI",
    )

    competencia = Competencia(
        ano=2026,
        mes=6,
    )

    estado = Estado(sigla="MG")

    item = ItemCatalogo(
        codigo="INS-001",
        descricao="Areia Média Lavada",
        tipo=TipoItem.INSUMO,
        catalogo=catalogo,
        unidade="M3"
    )

    with pytest.raises(ValueError, match="Preço não pode ser negativo"):
        PrecoItemCatalogo(
            item=item,
            estado=estado,
            preco_unitario=Decimal("-56.78"),
            fonte_precos=fonte_precos,
            competencia=competencia,
        )