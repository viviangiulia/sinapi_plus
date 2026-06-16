# Redes

## Conceitos

Uma Rede representa uma infraestrutura linear composta por um ou mais Trechos de Rede.

Cada Trecho de Rede possui:

* Uma Tubulação associada
* Um comprimento

Uma Tubulação é definida por:

* Material
* Diâmetro

---

## Comportamentos

### Consolidação de Quantitativos

Dada uma rede, o orçamento não deve considerar os trechos individualmente.

Os quantitativos devem ser obtidos através da consolidação dos comprimentos dos trechos por Tubulação.

Duas tubulações são consideradas equivalentes quando possuem o mesmo material e diâmetro.

---

### Regra de Quantificação

A quantidade orçamentária de uma tubulação corresponde à soma dos comprimentos de todos os trechos que utilizam a mesma especificação de tubulação.

Exemplo:

* Tubulação PBA DN 50

  * Trecho 1: 100 m
  * Trecho 2: 150 m

Quantidade consolidada:

* Tubulação PBA DN 50: 250 m

---

### Validação dos Trechos

Um trecho de rede não pode possuir comprimento negativo.

Tentativas de criação de trechos com comprimento inferior a zero devem resultar em erro de validação.

---

## Fluxo de Orçamentação
```bash
Rede
↓
Trechos de Rede
↓
Consolidação por Tubulação
↓
Quantitativos Consolidados
↓
Geração de Itens Orçamentários
↓
Orçamento
```
---

## Questões em Aberto

* Uma especificação orçamentária é identificada por:

  - Tipo de Rede?
  - Categoria?
  - Atributos Técnicos?

Ou existe um conceito único que encapsula tudo isso?



# Busca de Composição Orçamentária

## Objetivo

Converter um **Elemento Quantificável** em uma **Composição Quantificada**, associando a especificação técnica informada pelo usuário à composição correspondente cadastrada no catálogo.

---

## Conceitos Envolvidos

### Elemento Quantificável

Representa um quantitativo produzido pelo domínio a partir dos elementos do empreendimento.

Exemplos:

* Tubulação PBA DN 50 → 250 m
* Hidrômetro → 3 un
* Ligação Predial → 10 un

Estrutura conceitual:

```text
Categoria
Especificação
Quantidade
```

Exemplo:

```text
Categoria = TUBULACAO

Especificação:
    Material = PBA
    Diâmetro = 50

Quantidade = 250
```

---

### Catálogo de Composições

Responsável por localizar a composição correspondente a uma determinada especificação orçamentária.

Exemplo:

```text
Categoria = TUBULACAO
Material = PBA
Diâmetro = 50

↓

COMP-AGUA-003
```

---

### Composição Quantificada

Resultado da resolução da especificação no catálogo.

Estrutura conceitual:

```text
Código da Composição
Quantidade
```

Exemplo:

```text
Código = COMP-AGUA-003
Quantidade = 250
```

---

## Fluxo

```text
Elemento Quantificável
↓
Consulta ao Catálogo
↓
Composição Quantificada
```

Exemplo:

```text
Categoria = TUBULACAO
Material = PBA
Diâmetro = 50
Quantidade = 250

↓

Código = COMP-AGUA-003
Quantidade = 250
```

---

## Regras de Negócio

* A busca da composição deve ser realizada utilizando a categoria e sua especificação técnica.
* A quantidade não participa da seleção da composição.
* A quantidade deve ser preservada no resultado.
* O catálogo é responsável apenas por resolver especificações em códigos de composição.
* O catálogo não realiza cálculos de custo.

---

# TODO — Precificação das Composições

Após localizar a composição correspondente, o sistema deverá obter o custo unitário associado à composição para uma determinada localidade.

Fluxo futuro:

```text
Composição Quantificada
↓
Código da Composição
+
Estado
↓
Consulta de Custos
↓
Composição Precificada
```

Exemplo:

```text
Código = COMP-AGUA-003
Estado = MG

↓

Custo Unitário = R$ 127,35 / m
```

Questões ainda em aberto:

* Como representar o custo unitário no domínio.
* Como representar tabelas de custo por estado.
* Como calcular o custo total do item orçamentário.
* Como lidar com futuras regras de precificação (BDI, encargos, desoneração, ajustes regionais etc.).
