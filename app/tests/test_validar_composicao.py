import pytest
from app.models import ComponenteComposicao, ItemCatalogo, TipoItem,Composicao


def test_coeficiente_nao_pode_ser_negativo():
    item = ItemCatalogo(
        codigo="INS-001", descricao="Tubo PBA DN 50", tipo=TipoItem.INSUMO
    )

    with pytest.raises(ValueError):
        ComponenteComposicao(item=item, coeficiente=-50)


def test_composicao_deve_possuir_componentes():
    
    with pytest.raises(ValueError):
       Composicao(
        codigo="COMP-PAV-004",
        descricao="Pavimentação CBUQ Capa 5cm",
        items=[]
    )


def test_item_catalogo_deve_ter_codigo_valido():
    
    with pytest.raises(ValueError):
       ItemCatalogo(
        codigo="",
        descricao="Areia Média Lavada",
        tipo=TipoItem.INSUMO
    )
