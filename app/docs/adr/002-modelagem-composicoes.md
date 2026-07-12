# ADR-002 — Modelagem de Composições e Estrutura de Custos

## Status

Aceito

---

## Contexto

Inicialmente as composições eram tratadas apenas como identificadores retornados pelo catálogo de composições.

Exemplo:

```text
Elemento Quantificável
↓
Resolução da Composição
↓
COMP-AGUA-003
```

Entretanto, durante a análise das regras de precificação, foi identificado que uma composição não representa apenas um código.

Uma composição possui estrutura própria e é formada por insumos e/ou composições secundárias associados a coeficientes de consumo.

---

## Problema

A precificação não é realizada diretamente sobre a composição principal.

O cálculo ocorre através dos componentes que formam a composição.

Exemplo:

```text
COMP-AGUA-003

├── INS-001 (Areia Média)      coeficiente = 0.50
├── INS-002 (Cimento)          coeficiente = 2.00
└── COMP-123 (Argamassa)       coeficiente = 0.30
```

Para cada componente é obtido um preço unitário.

O custo unitário da composição é calculado por:

```text
Σ (coeficiente × preço_unitário)
```

O custo total da composição quantificada é calculado por:

```text
quantidade × custo_unitário
```

---

## Decisão 1 — Modelar explicitamente a Composição

### Decisão

A composição passa a ser modelada explicitamente no domínio.

Ela deixa de ser tratada apenas como um código retornado pelo catálogo.

### Justificativa

A composição representa um conceito central do domínio.

Ela contém:

* Código
* Descrição
* Estrutura de componentes
* Regras para formação do custo

Tratar a composição apenas como uma string impediria representar a origem dos custos e os cálculos intermediários necessários para auditoria e análise.

### Consequências

* Permite rastrear a formação dos custos.
* Permite representar a estrutura real das CPUs.
* Facilita validação e depuração dos cálculos.
* Aproxima o modelo da realidade do domínio.

---

## Decisão 2 — Representar componentes através de um Value Object

### Decisão

A participação de um item dentro de uma composição será representada por um Value Object denominado `ComponenteComposicao`.

Estrutura conceitual:

```text
ComponenteComposicao
├── item
└── coeficiente
```

### Justificativa

O coeficiente não pertence ao item em si.

O coeficiente pertence à relação entre o item e a composição.

Exemplo:

```text
INS-AREIA
```

Pode participar de diferentes composições:

```text
Concreto
coeficiente = 0.65
```

```text
Argamassa
coeficiente = 0.18
```

O item continua sendo o mesmo.

O que muda é sua participação dentro da composição.

Portanto o coeficiente deve pertencer ao componente da composição e não ao item do catálogo.

### Consequências

* Evita duplicação de itens.
* Permite reutilização de insumos e composições.
* Representa corretamente a relação entre composição e coeficiente.
* Facilita futuras evoluções da estrutura de custos.

---

## Decisão 3 — Unificar Insumos e Composições Secundárias em um Item de Catálogo

### Decisão

Criar uma entidade genérica denominada `ItemCatalogo`.

Estrutura conceitual:

```text
ItemCatalogo
├── codigo
├── descricao
└── tipo
```

Onde:

```text
TipoItem
├── INSUMO
└── COMPOSICAO
```

### Justificativa

Uma composição pode ser formada tanto por:

* Insumos
* Composições secundárias

Ambos possuem características semelhantes:

* Código
* Descrição
* Identidade própria

A principal diferença é sua classificação.

Exemplos:

```text
INS-001
Areia Média
Tipo = INSUMO
```

```text
COMP-123
Argamassa
Tipo = COMPOSICAO
```

Utilizar uma única entidade reduz duplicação e simplifica a estrutura do domínio.

### Consequências

* Modelo mais simples.
* Menor duplicação de conceitos.
* Facilita navegação e consulta dos componentes.
* Permite representar insumos e composições secundárias de forma uniforme.

---

## Estrutura Resultante

```text
Composicao
├── codigo
├── descricao
└── componentes
      │
      ▼
ComponenteComposicao
├── item
└── coeficiente
      │
      ▼
ItemCatalogo
├── codigo
├── descricao
└── tipo
```

---

## Fluxo de Precificação Identificado

Fluxo previsto para cálculo dos custos:

```text
Elemento Quantificável
↓
Resolução da Composição
↓
Composição Quantificada
↓
Obtenção da Estrutura da Composição
↓
Obtenção dos Preços dos Componentes
↓
Cálculo do Custo Unitário
↓
Cálculo do Custo Total
↓
Item Orçamentário
```

---

## Questões em Aberto

### OQ-004 — Representação dos Preços Unitários

Ainda não foi definida a modelagem responsável por representar os preços associados aos itens de catálogo para uma determinada localidade.

Exemplo:

```text
INS-001
+
MG
↓
Preço Unitário
```

---

### OQ-005 — Estratégia de Precificação

Ainda não foi definida a responsabilidade pela execução do cálculo:

```text
Σ (coeficiente × preço_unitário)
```

e posterior cálculo:

```text
quantidade × custo_unitário
```

A modelagem será revisitada após a definição do mecanismo de consulta de preços por estado.
