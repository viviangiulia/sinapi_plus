"""Mapeamento dos diferentes tipos de itens da rede de água e regras para acessar as composições associadas a cada um."""

CONFIG_AGUA = {
    "simples": {
        "input_agua_ligacao_predial": "COMP-AGUA-001",
        "input_agua_hidrometro": "COMP-AGUA-002",
    },

    "redes": {
        "pba": {
            "input_qtd": "input_agua_qtd_trechos_pba",
            "input_diametro": "input_agua_diametro_pba_",
            "input_comprimento": "input_agua_comprimento_pba_",
            "mapa_composicao": {
                50: "COMP-AGUA-003",
                75: "COMP-AGUA-004",
                100: "COMP-AGUA-005",
            },
        },

        "defofo": {
            "input_qtd": "input_agua_qtd_trechos_defofo",
            "input_diametro": "input_agua_diametro_defofo_",
            "input_comprimento": "input_agua_comprimento_defofo_",
            "mapa_composicao": {
                150: "COMP-AGUA-006",
                200: "COMP-AGUA-007",
                250: "COMP-AGUA-008",
                300: "COMP-AGUA-009",
            },
        }
    }
}
