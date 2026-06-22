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

# OQ-002 — Adoção de Repository Pattern

## Contexto

Atualmente a aplicação realiza a leitura das bases de dados através de arquivos Excel (`.xlsx`).

A leitura é executada durante a inicialização da aplicação e os dados são carregados em memória, sendo posteriormente armazenados em cache e no `session_state`.

---

## Esquema Atual de Carregamento

```text
carregar_arquivos
↓
leitura da base de preços
↓
leitura da base de composições
↓
armazenamento em cache / session_state
```

---

## Problemas Identificados

### Upload Manual de Arquivos

Atualmente as bases precisam ser enviadas para o repositório para atualização dos dados.

Consequências:

* Necessidade de Pull Request para atualização das bases.
* Dificuldade para atualização frequente dos dados.
* Dependência do ciclo de deploy da aplicação.

---

### Persistência Acoplada ao Excel

Atualmente a única forma de leitura disponível é através de arquivos Excel.

Consequências:

* Dependência direta de `pd.read_excel`.
* Dificuldade de migração para banco de dados.
* Dificuldade de integração com APIs ou outras fontes de dados.

---

### Regras de Negócio Acopladas a DataFrames

Atualmente parte das regras de negócio é implementada diretamente sobre estruturas de DataFrame.

Consequências:

* Forte acoplamento à estrutura física dos dados.
* Maior dificuldade para testes unitários.
* Menor expressividade do modelo de domínio.
* Dificuldade de separação entre domínio e infraestrutura.

---

## Hipótese de Evolução

Introduzir abstrações de Repository responsáveis por:

1. Recuperar os dados da origem de persistência.
2. Converter os dados para objetos do domínio.
3. Isolar o domínio dos detalhes de armazenamento.

Objetivo:

```text
Domínio
↓
Repository
↓
Infraestrutura
```

Ao invés de:

```text
Domínio
↓
DataFrame / Excel
↓
Persistência
```

---

## Possíveis Repositories

### CatalogoComposicoesRepository

Responsável por recuperar:

* Composições
* Componentes da composição
* Coeficientes

Retorna objetos do domínio:

```text
Composicao
ComponenteComposicao
ItemCatalogo
```

---

### CatalogoPrecosRepository

Responsável por recuperar:

* Preços dos itens de catálogo
* Preços por estado

Retorna objetos do domínio:

```text
PrecoItemCatalogo
```

---

### CatalogoElementosRepository

Responsável por resolver especificações em composições orçamentárias.

Exemplo:

```text
ElementoQuantificavel
↓
Código de Composição
```

**Observação:** nome e responsabilidade ainda em investigação.

---

### OrcamentosRepository

Responsável pela persistência das simulações realizadas.

Exemplos:

* Salvar orçamento.
* Recuperar orçamento.
* Duplicar orçamento.
* Consultar simulações anteriores.

Retorna objetos do domínio:

```text
Orcamento
ComposicaoPrecificada
```

---

## Possíveis Benefícios

* Modelo mais expressivo.
* Redução de acoplamento.
* Maior aderência ao princípio da inversão de dependências (DIP).
* Facilidade para testes unitários.
* Flexibilidade para troca de mecanismos de persistência.
* Evolução futura para SQLAlchemy e PostgreSQL sem impacto no domínio.

---

## Possíveis Desvantagens

* Maior número de classes.
* Maior complexidade arquitetural.
* Necessidade de mapeamento entre estruturas persistidas e objetos do domínio.
* Curva de aprendizado adicional.

---

## Questões em Aberto

* Todos os catálogos devem possuir repositories independentes?
* Os repositories devem retornar exclusivamente objetos do domínio?
* Como será realizado o mapeamento entre estruturas persistidas e objetos do domínio?
* Quais repositories serão necessários na primeira versão do sistema?
* Existe necessidade de abstrações adicionais para escrita e atualização de dados?

---

## Decisão Provisória

Não introduzir banco de dados neste momento.

Priorizar a introdução das abstrações de Repository utilizando as bases atuais em DataFrame como mecanismo de persistência.

Após estabilização do modelo de domínio e dos repositories, reavaliar a adoção de SQLAlchemy e PostgreSQL.
