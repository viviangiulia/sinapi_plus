# ADR-003 — OrcamentoRepository e Persistência de Simulações

## Status

Proposto

---

## Contexto

Durante a modelagem do domínio foram identificados dois grupos distintos de dados:

### Catálogos de Referência

Dados mantidos externamente à aplicação e utilizados durante o processo de orçamento.

Exemplos:

* Composições
* Insumos
* Preços SINAPI
* Regras de resolução de especificações

Esses dados são consumidos pela aplicação, mas não são criados ou alterados por ela.

Repositories identificados:

* ComposicaoRepository
* PrecoRepository
* CatalogoElementosRepository

---

### Dados Gerados pela Aplicação

Dados produzidos pelo próprio SINAPI+ durante a execução das simulações.

Exemplos:

* Entradas de uma simulação
* Composições precificadas
* Resultado final do orçamento
* Cenários salvos pelo usuário

Esses dados poderão necessitar persistência para consulta e reaproveitamento futuro.

---

## Problema

Embora a necessidade de persistência de simulações já tenha sido identificada, o agregado `Orcamento` ainda não está completamente modelado.

Atualmente ainda existem dúvidas sobre:

* Quais informações pertencem ao orçamento.
* Como representar cenários e versões.
* Quais entradas devem ser persistidas.
* Como será realizado o reaproveitamento de simulações anteriores.

Implementar um `OrcamentoRepository` neste momento introduziria uma abstração antes da definição completa do agregado responsável por ela.

---

## Decisão

Adiar a implementação do `OrcamentoRepository`.

Neste momento serão implementados apenas os repositories necessários para consulta dos catálogos utilizados pelo domínio:

* ComposicaoRepository
* PrecoRepository

O `OrcamentoRepository` será introduzido após estabilização da modelagem do agregado `Orcamento`.

---

## Justificativa

Os repositories atualmente implementados resolvem problemas já existentes:

```text
Código da composição
↓
ComposicaoRepository
↓
Composicao
```

```text
Item + Estado
↓
PrecoRepository
↓
PrecoItemCatalogo
```

Já a persistência de orçamentos representa uma necessidade futura que depende da definição de conceitos ainda em investigação.

---

## Possíveis Responsabilidades Futuras

O `OrcamentoRepository` poderá ser responsável por:

* Salvar simulações.
* Recuperar simulações.
* Duplicar simulações.
* Listar simulações existentes.
* Recuperar versões anteriores.
* Persistir parâmetros de entrada.

Exemplo conceitual:

```text
Orcamento
↓
OrcamentoRepository
↓
Banco de Dados
```

---

## Questões em Aberto

### O que constitui um Orcamento?

Possíveis atributos:

* Identificador
* Data de criação
* Estado
* Lista de composições precificadas
* Custo total
* Parâmetros de entrada
* Versão da base utilizada

---

### Qual o nível de persistência desejado?

Persistir apenas o resultado final:

```text
Orcamento
↓
Custo Total
```

ou persistir toda a memória de cálculo:

```text
Entradas
↓
Composições
↓
Preços
↓
Resultado
```

---

### Como implementar o reaproveitamento de simulações?

Necessário definir:

* Duplicação de cenários.
* Histórico de alterações.
* Versionamento.

---

## Consequências

### Positivas

* Evita abstrações prematuras.
* Permite amadurecimento do domínio antes da persistência.
* Mantém foco na implementação do fluxo principal de orçamento.

### Negativas

* Persistência de simulações permanece indisponível.
* Necessidade de futura refatoração ao introduzir o agregado Orcamento.

```
```
