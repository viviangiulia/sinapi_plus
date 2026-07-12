# Fluxo Atual do SINAPI+

## Visão Geral

O objetivo do sistema é transformar elementos reais de engenharia em um orçamento precificado.

Fluxo principal:

```text
Dados de Entrada
↓
ElementoQuantificavel
↓
ComposicaoQuantificada
↓
Composicao
↓
ComposicaoPrecificada
↓
Orcamento
```

---

# 1. Dados de Entrada

## Descrição

Os dados de entrada são compostos por:

* Lista de Elementos Quantificáveis.
* Estado utilizado como referência geográfica para precificação.

O ElementoQuantificavel representa a execução real de um serviço.

Exemplos:

* Tubulação.
* Pavimentação.
* Poço de visita.
* Rede de água.
* Rede de esgoto.

---

## Status

| Item                | Status                                   |
| ------------------- | ---------------------------------------- |
| Classe modelada     | ✅                                        |
| Testes unitários    | ✅                                        |
| Totalmente modelado | ⚠️ Parcial                               |
| Questões em aberto  | Especialização futura das especificações |

---

# 2. Conversão para Composição Quantificada

## Descrição

Cada ElementoQuantificavel possui uma categoria e um conjunto de especificações.

Essas informações são utilizadas para localizar o código da composição correspondente.

Exemplo:

```text
TUBULACAO
Material = PBA
Diametro = 50
↓
COMP-AGUA-003
```

O resultado dessa etapa é uma ComposicaoQuantificada.

---

## Status

| Item                    | Status                                       |
| ----------------------- | -------------------------------------------- |
| Classe modelada         | ✅                                            |
| Repository implementado | ❌                                            |
| Testes unitários        | ✅                                            |
| Totalmente modelado     | ⚠️ Parcial                                   |
| Questões em aberto      | Implementação do CatalogoElementosRepository |

---

# 3. Busca da Composição

## Descrição

A partir do código da composição é realizada uma consulta ao ComposicaoRepository.

O resultado é uma Composicao contendo:

* Código.
* Descrição.
* Lista de componentes.
* Coeficientes.

Exemplo:

```text
COMP-AGUA-003
↓
Composicao
 ├── Tubo PBA
 ├── Areia
 └── Escavação
```

---

## Status

| Item                    | Status                         |
| ----------------------- | ------------------------------ |
| Classe modelada         | ✅                              |
| Repository implementado | ✅                              |
| Testes unitários        | ❌                              |
| Totalmente modelado     | ✅                              |
| Questões em aberto      | Definição de testes unitários |

---

# 4. Precificação da Composição

## Descrição

Cada componente da composição possui um ItemCatalogo associado.

O preço é obtido através do PrecoRepository utilizando:

* Código do item.
* Estado.

O custo unitário da composição é calculado pela soma:

```text
coeficiente × preço
```

para todos os componentes.

O resultado é uma ComposicaoPrecificada.

---

## Status

| Item                         | Status                                |
| ---------------------------- | ------------------------------------- |
| Classes principais modeladas | ✅                                     |
| Repository implementado      | ✅                                     |
| Testes unitários             | ❌                                      |
| Totalmente modelado          | ⚠️ Parcial                            |
| Questões em aberto           | Consolidação do ComponentePrecificado,Definição de testes unitários |

---

# 5. Orçamento

## Descrição

O orçamento representa o resultado final do processo.

Hipótese atual:

```text
Orcamento
 ├── id
 ├── composicoes_precificadas
 └── custo_total
```

O custo total corresponde à soma dos custos totais das composições precificadas.

---

## Status

| Item                    | Status                         |
| ----------------------- | ------------------------------ |
| Classe modelada         | ⚠️ Inicial                     |
| Repository implementado | ❌                              |
| Testes unitários        | ❌                              |
| Totalmente modelado     | ❌                              |
| Questões em aberto      | Estrutura completa do agregado |

---

# Avaliação Geral da Modelagem

## Pontos Positivos

* Fluxo principal do domínio identificado.
* Linguagem do domínio consistente.
* Separação entre resolução de composição e precificação.
* Repositories introduzidos de forma gradual.
* Modelo compatível com múltiplos tipos de infraestrutura.
* Base sólida para introdução futura de Service Layer.

---

## Pontos de Atenção

* Especialização futura das especificações.
* Consolidação do conceito de ComponentePrecificado.
* Descoberta completa do agregado Orcamento.
* Definição futura de persistência e versionamento de simulações.

---

## Próxima Investigação

Identificar qual componente será responsável por coordenar o fluxo:

```text
ElementoQuantificavel
↓
ComposicaoQuantificada
↓
Composicao
↓
ComposicaoPrecificada
↓
Orcamento
```

Hipótese inicial:

```text
Service Layer
```
