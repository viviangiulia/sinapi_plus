from app.models import ComposicaoQuantificada, ElementoQuantificavel, Especificacao
from typing import Dict
from dataclasses import dataclass


@dataclass
class CatalogoFake:
    catalogo: Dict

    def resolver_composicao(self, elemento: ElementoQuantificavel):
        if all(valor is None for valor in vars(elemento.especificacao).values()):

            return ComposicaoQuantificada(
                codigo_composicao=self.catalogo[elemento.categoria],
                quantidade=elemento.quantidade,
            )
        return ComposicaoQuantificada(
            codigo_composicao=self.catalogo[elemento.categoria][elemento.especificacao],
            quantidade=elemento.quantidade,
        )


def test_encontrar_composicao_para_hidrometro():
    catalogo = CatalogoFake({"HIDROMETRO": "COMP-AGUA-002"})

    elemento = ElementoQuantificavel(
        especificacao=Especificacao(),
        categoria="HIDROMETRO",
        quantidade=3,
    )

    composicao_quantificada = catalogo.resolver_composicao(elemento)

    assert composicao_quantificada.codigo_composicao == "COMP-AGUA-002"
    assert composicao_quantificada.quantidade == 3


def test_encontrar_composicao_para_tubo_pba_50():
    catalogo = CatalogoFake(
        {
            "TUBULACAO": {
                Especificacao(
                    material="PBA",
                    diametro=50,
                ): "COMP-AGUA-003"
            }
        }
    )

    elemento = ElementoQuantificavel(
        especificacao=Especificacao(
            material="PBA",
            diametro=50,
        ),
        categoria="TUBULACAO",
        quantidade=56,
    )

    composicao_quantificada = catalogo.resolver_composicao(elemento)

    assert composicao_quantificada.codigo_composicao == "COMP-AGUA-003"
    assert composicao_quantificada.quantidade == 56