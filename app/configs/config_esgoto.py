"""Mapeamento dos diferentes tipos de itens da rede de esgoto e regras para acessar as composições associadas a cada um."""

CONFIG_ESGOTO = {
    "simples": {
        "input_esgoto_qtd_ligacao_4m": "COMP-ESGOTO-006",
        "input_esgoto_qtd_ligacao_6m": "COMP-ESGOTO-008",
        "input_esgoto_pv_max_150": "COMP-ESGOTO-003",
        "input_esgoto_pv_max_200": "COMP-ESGOTO-007",
        "input_esgoto_pv_max_250": "COMP-ESGOTO-004",
        "input_esgoto_pv_max_300": "COMP-ESGOTO-005",
    },
    "redes": {
        "ocre": {
            "input_qtd": "input_esgoto_qtd_trechos_ocre",
            "input_diametro": "input_esgoto_diametro_ocre_",
            "input_comprimento": "input_esgoto_comprimento_ocre_",
            "mapa_composicao": {
                100: "COMP-ESGOTO-009",
                150: "COMP-ESGOTO-010",
                200: "COMP-ESGOTO-011",
                250: "COMP-ESGOTO-012",
                300: "COMP-ESGOTO-013",
                350: "COMP-ESGOTO-014",
            },
        }
    },
}
