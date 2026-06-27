# ADR-004 — Introdução da Service Layer e Fluxo de Geração de Orçamentos

## Status

Aceito

---

## Contexto

Até o momento o projeto possuía:

* Modelo de domínio;
* Repositories responsáveis pela consulta de dados;
* Objetos representando composições, preços e orçamento.

Entretanto, ainda não existia uma camada responsável por coordenar o fluxo completo de geração de um orçamento.

A lógica encontrava-se distribuída entre objetos isolados, sem representar explicitamente o caso de uso principal da aplicação.

---

## Decisão

Foi introduzida uma camada de serviço através da função:

```python
gerar_orcamento(...)
```

A responsabilidade desta camada é exclusivamente orquestrar o caso de uso **Gerar Orçamento**, delegando todas as regras de negócio aos objetos do domínio e aos repositories.

O fluxo adotado passa a ser:

```text
ElementoQuantificavel
        │
        ▼
CatalogoRepository
        │
        ▼
ComposicaoQuantificada
        │
        ▼
ComposicaoRepository
        │
        ▼
Composicao
        │
        ▼
PrecoRepository
        │
        ▼
ComponentePrecificado
        │
        ▼
ComposicaoPrecificada
        │
        ▼
Orcamento
```

A Service Layer não executa cálculos de negócio.

Seu papel limita-se a:

* localizar a composição correspondente ao elemento;
* recuperar a estrutura da composição;
* consultar os preços dos componentes;
* montar os objetos do domínio;
* produzir o orçamento final.

---

## Alterações realizadas

### CatalogoRepository

Foi criado o `CatalogoRepository`, responsável por converter um `ElementoQuantificavel` em uma `ComposicaoQuantificada`.

A resolução ocorre através da combinação entre:

* categoria;
* atributos presentes na especificação.

Essa decisão desacopla o domínio da estrutura tabular utilizada para armazenar o catálogo.

---

### Organização das bases

As planilhas utilizadas pelos repositories foram reorganizadas para refletir melhor as responsabilidades do domínio.

Em especial:

* catálogo de elementos;
* base de composições.

A estrutura passou a favorecer consultas baseadas nas características do elemento, simplificando a implementação dos repositories.

---

### Estrutura de testes

Os testes passaram a ser concentrados na pasta:

```text
app/tests
```

centralizando a validação do domínio e da camada de aplicação.

---

## Consequências

### Positivas

* Caso de uso principal explicitamente modelado.
* Separação clara entre domínio, persistência e aplicação.
* Repositories possuem responsabilidades únicas.
* Fluxo de orçamento tornou-se facilmente compreensível.
* Facilidade para criação de novos casos de uso.

### Negativas

* O `OrcamentoService` ainda instancia diretamente os repositories.
* Ainda não existe mecanismo de injeção de dependências.
* Persistência do orçamento permanece pendente.

---

## Questões em aberto

* Definir a interface definitiva do `OrcamentoRepository`.
* Introduzir persistência utilizando SQLAlchemy.
* Avaliar mecanismo de Dependency Injection.
* Refinar as especializações de `Especificacao`.
* Avaliar especialização futura da camada de serviço conforme novos casos de uso sejam introduzidos.
