# ADR-001 — Modelagem de Redes e Resolução de Composições

## Status

Aceito

---

## Contexto

Durante a modelagem inicial do domínio de orçamentação de infraestrutura foram identificadas duas dúvidas principais:

1. Uma Rede deveria possuir apenas um tipo de tubulação ou permitir múltiplos materiais e diâmetros.
2. A lógica de seleção de composições deveria pertencer aos objetos do domínio ou a um componente especializado.

---

## Decisão 1 — Rede como conceito único do domínio

### Decisão

Modelar Água, Esgoto e Drenagem através de uma única entidade `Rede`.

A entidade possui um atributo de classificação (`escopo_rede`) que identifica o contexto da rede.

### Justificativa

Os comportamentos observados até o momento são idênticos:

```text
Trechos
↓
Agrupamento por Tubulação
↓
Geração de Elementos Quantificáveis
```

Não foram identificadas regras de negócio que justifiquem a existência de entidades distintas para:

* Rede de Água
* Rede de Esgoto
* Rede de Drenagem

A principal diferença observada atualmente está no catálogo de composições utilizado para resolver as especificações orçamentárias.

Portanto, o comportamento de domínio permanece concentrado em uma única entidade `Rede`, evitando duplicação de lógica.

### Consequências

* Elimina duplicação de comportamento entre tipos de rede.
* Permite reutilização da mesma lógica de agregação e quantificação.
* Facilita manutenção e evolução do domínio.
* Novos tipos de rede poderão ser incorporados sem necessidade de criação de novas entidades.
* Caso comportamentos específicos surjam no futuro, a modelagem poderá ser reavaliada.

---

## Decisão 2 — Rede composta por múltiplas tubulações

### Decisão

Permitir que uma Rede seja composta por múltiplos Trechos de Rede, cada um possuindo sua própria Tubulação.

### Justificativa

Uma rede real pode conter:

* Materiais distintos.
* Diâmetros distintos.
* Combinações variadas de ambos.

O comportamento de agregação é realizado sobre os Trechos, consolidando comprimentos por Tubulação.

Exemplo:

```text
Rede de Água

├── PBA DN 50 -> 250 m
├── PBA DN 75 -> 5 m
└── DEFOFO DN 150 -> 300 m
```

O quantitativo utilizado para orçamento é obtido através da consolidação dos comprimentos de trechos que compartilham a mesma especificação de tubulação.

### Consequências

* O modelo representa adequadamente a realidade de engenharia.
* Evita restrições artificiais no domínio.
* Permite geração correta dos quantitativos orçamentários.
* Permite que novas combinações de materiais e diâmetros sejam incorporadas sem alteração estrutural do modelo.

---

## Decisão 3 — Resolução de composição através de componente especializado

### Decisão

A seleção da composição não será responsabilidade da Rede nem da Tubulação.

Será responsabilidade de um componente especializado de resolução de composições.

### Justificativa

Tubulações possuem responsabilidade de representar características técnicas:

* Material
* Diâmetro

A lógica de busca em catálogos é uma responsabilidade distinta:

```text
Elemento Quantificável
↓
Consulta ao Catálogo
↓
Composição Quantificada
```

O domínio produz os quantitativos necessários para orçamento, enquanto a resolução da composição é responsável por transformar uma especificação orçamentária em um código de composição.

Separar essas responsabilidades reduz acoplamento e facilita a evolução da solução.

### Consequências

* O domínio permanece independente da forma de armazenamento das composições.
* A implementação poderá evoluir posteriormente para Repository Pattern.
* Facilita testes unitários utilizando catálogos simulados (`CatalogoFake`).
* Permite trocar a origem dos dados (Excel, DataFrame, SQLite, API, etc.) sem alterar a modelagem do domínio.

---

## Questões em Aberto

### OQ-001 — Representação das Especificações Técnicas

Atualmente existe uma única estrutura de especificação utilizada para resolução de composições.

É necessário investigar se a evolução do domínio justificará uma hierarquia de especificações especializadas por categoria.

Exemplos:

```text
EspecificacaoTubulacao
EspecificacaoPocoVisita
EspecificacaoBocaDeLobo
EspecificacaoPavimentacao
```

---

### OQ-002 — Representação do Catálogo de Composições

Definir a implementação definitiva do catálogo utilizado para resolução das composições.

Alternativas previstas:

* DataFrame
* Excel
* SQLite
* API
* Repository Pattern

---

### OQ-003 — Precificação das Composições

Após a resolução da composição, o sistema deverá obter o custo unitário correspondente para uma determinada localidade.

Fluxo previsto:

```text
Elemento Quantificável
↓
Composição Quantificada
↓
Consulta de Custos
↓
Composição Precificada
```

Ainda é necessário definir:

* Como representar custos unitários no domínio.
* Como representar tabelas regionais de preços.
* Como modelar a etapa de precificação antes da geração do orçamento final.

```
```
