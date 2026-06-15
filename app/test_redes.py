import pytest
from models import Rede, TrechoRede, Tubulacao


def test_consolidar_comprimentos_por_tubulacao():
    trechos_agua = [
        TrechoRede(
            tubulacao=Tubulacao(material="PBA", diametro=50), id=1, comprimento=100
        ),
        TrechoRede(
            tubulacao=Tubulacao(material="PBA", diametro=50), id=2, comprimento=150
        ),
        TrechoRede(
            tubulacao=Tubulacao(material="PBA", diametro=75), id=3, comprimento=5
        ),
        TrechoRede(
            tubulacao=Tubulacao(material="DEFOFO", diametro=150), id=4, comprimento=300
        ),
    ]
    rede = Rede(escopo_rede="ÁGUA", trechos=trechos_agua)
    tubulacao_pba_50 = Tubulacao(material="PBA", diametro=50)
    tubulacao_pba_75 = Tubulacao(material="PBA", diametro=75)
    tubulacao_defofo_150 = Tubulacao(material="DEFOFO", diametro=150)

    assert rede.comprimentos_rede_por_tubulacao[tubulacao_pba_50] == 250
    assert rede.comprimentos_rede_por_tubulacao[tubulacao_pba_75] == 5
    assert rede.comprimentos_rede_por_tubulacao[tubulacao_defofo_150] == 300


def test_comprimento_trecho_invalido():
    with pytest.raises(ValueError):
        TrechoRede(
            tubulacao=Tubulacao(material="DEFOFO", diametro=100),
            id=3,
            comprimento=-30,
        )


def test_converter_rede_em_elementos_quantificaveis():
    trechos_agua = [
        TrechoRede(
            tubulacao=Tubulacao(material="PBA", diametro=50),
            id=1,
            comprimento=100,
        ),
        TrechoRede(
            tubulacao=Tubulacao(material="PBA", diametro=50),
            id=2,
            comprimento=150,
        ),
        TrechoRede(
            tubulacao=Tubulacao(material="PBA", diametro=75),
            id=3,
            comprimento=5,
        ),
        TrechoRede(
            tubulacao=Tubulacao(material="DEFOFO", diametro=150),
            id=4,
            comprimento=300,
        ),
    ]

    rede = Rede(
        escopo_rede="AGUA",
        trechos=trechos_agua,
    )

    elementos = rede.gerar_elementos_quantificaveis()

    assert len(elementos) == 3

    elemento_pba_50 = next(
        e
        for e in elementos
        if e.especificacao.material == "PBA" and e.especificacao.diametro == 50
    )

    elemento_pba_75 = next(
        e
        for e in elementos
        if e.especificacao.material == "PBA" and e.especificacao.diametro == 75
    )

    elemento_defofo_150 = next(
        e
        for e in elementos
        if e.especificacao.material == "DEFOFO" and e.especificacao.diametro == 150
    )

    assert elemento_pba_50.quantidade == 250
    assert elemento_pba_75.quantidade == 5
    assert elemento_defofo_150.quantidade == 300

    assert all(elemento.categoria == "TUBULACAO" for elemento in elementos)
