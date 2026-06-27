from models import PrecoItemCatalogo, ItemCatalogo, TipoItem, Estado
from typing import Dict
from dataclasses import dataclass
import pytest

# Dado um estado e um item devo encontrar
# Preço
@dataclass
class CatalogoFakePrecos:
    catalogo: Dict

    def buscar_preco(self, item: ItemCatalogo, estado: Estado):
        codigo_item = item.codigo
        preco_unit = self.catalogo[estado][codigo_item]
        return PrecoItemCatalogo(item=item, estado=estado, preco_unitario=preco_unit)


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

    item = ItemCatalogo(
        codigo="INS-001", descricao="Areia Média Lavada", tipo=TipoItem.INSUMO
    )

    preco_item = catalogo_precos.buscar_preco(item, "SP")

    assert preco_item.preco_unitario == 18.20


def test_preco_deve_ser_positivo():
    item = ItemCatalogo(
        codigo="INS-001", descricao="Areia Média Lavada", tipo=TipoItem.INSUMO
    )
    with pytest.raises(ValueError):
        PrecoItemCatalogo(
            item=item,
            estado="MG",
            preco_unitario=-56.78
        )