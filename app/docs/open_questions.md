# Open Questions

## OQ-001 — Representação de Especificações Técnicas

### Contexto

Atualmente o domínio possui uma única classe `Especificacao` utilizada para representar os atributos necessários para resolução de composições no catálogo.

Exemplo atual:

```text
Especificacao
├── material
├── diametro
└── profundidade
```

Entretanto, durante a expansão do domínio, observou-se que diferentes categorias de elementos orçamentários possuem conjuntos distintos de atributos.

---

### Exemplos Identificados

| Categoria      | Possíveis Atributos |
| -------------- | ------------------- |
| Tubulação      | material, diâmetro  |
| Poço de Visita | profundidade        |
| Boca de Lobo   | possui_grelha       |
| Pavimentação   | material, espessura |
| Hidrômetro     | nenhum              |

---

### Problema

A evolução da classe atual pode resultar em uma estrutura contendo diversos atributos opcionais que não possuem significado para todas as categorias.

Exemplo:

```text
Especificacao(
    material="PBA",
    diametro=50,
    profundidade=None,
    possui_grelha=None,
    espessura=None,
)
```

---

### Hipótese de Evolução

Investigar a utilização de uma hierarquia de especificações especializadas.

Exemplo conceitual:

```text
Especificacao
├── EspecificacaoTubulacao
├── EspecificacaoPocoVisita
├── EspecificacaoBocaDeLobo
├── EspecificacaoPavimentacao
└── EspecificacaoHidrometro
```

Cada especificação possuiria apenas os atributos relevantes para sua categoria.

---

### Possíveis Benefícios

* Modelo mais expressivo.
* Redução de atributos opcionais.
* Validações específicas por categoria.
* Melhor aderência ao domínio.

---

### Possíveis Desvantagens

* Maior número de classes.
* Catálogo de composições precisa lidar com múltiplos tipos de especificação.
* Complexidade adicional de modelagem.

---

### Decisão Atual

Não implementar neste momento.

Aguardar modelagem de mais categorias do domínio para avaliar se a diversidade de atributos justifica a criação de uma hierarquia de especificações.
