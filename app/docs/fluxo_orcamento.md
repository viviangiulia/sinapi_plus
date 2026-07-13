# Fluxo de Orçamento do SINAPI+

## Visão Geral

O objetivo do sistema é transformar composições selecionadas pelo usuário em um orçamento estruturado e precificado a partir de um determinado contexto de precificação.

O fluxo principal atual é:

```text
Seleção das Composições
        ↓
ComposicaoQuantificada
        ↓
ComposicaoRepository
        ↓
Composicao
        ↓
PrecoRepository
        ↓
PrecoItemCatalogo
        ↓
ComponentePrecificado
        ↓
ComposicaoPrecificada
        ↓
Orcamento
```

O fluxo é coordenado pela **Service Layer**, através do caso de uso `gerar_orcamento`.

A arquitetura busca manter:

- regras de negócio independentes das fontes de dados;
- domínio independente da persistência;
- domínio independente da futura API;
- domínio independente da interface gráfica;
- separação entre catálogo de itens e fontes de preços;
- possibilidade de evolução para diferentes catálogos e fontes de preços.

---

# 1. Dados de Entrada

## Descrição

O caso de uso de geração de orçamento recebe as composições selecionadas pelo usuário e o contexto necessário para realizar a precificação.

A assinatura conceitual atual é:

```text
gerar_orcamento(
    nome,
    descricao,
    estado,
    fonte_precos,
    catalogo,
    competencia,
    composicoes_orcamento
)
```

As informações recebidas podem ser divididas em três grupos:

```text
Identificação do orçamento
├── nome
└── descricao

Contexto de precificação
├── estado
├── fonte_precos
└── competencia

Seleção do orçamento
├── catalogo
└── composicoes_orcamento
```

A lista de composições representa os serviços selecionados pelo usuário para fazer parte do orçamento.

---

## Seleção direta de composições

Na abordagem atual, o usuário seleciona diretamente as composições que deseja utilizar.

Cada seleção é representada por uma `ComposicaoQuantificada`:

```text
ComposicaoQuantificada
├── codigo_composicao
└── quantidade
```

Exemplo:

```text
ComposicaoQuantificada
├── codigo_composicao = COMP-AGUA-003
└── quantidade = 150.0
```

A quantidade representa quanto daquela composição será considerado no orçamento.

A quantidade não pode ser negativa.

---

## Decisão de simplificação do fluxo

Anteriormente, o domínio possuía um fluxo de resolução automática:

```text
ElementoQuantificavel
        ↓
CatalogoRepository
        ↓
ComposicaoQuantificada
```

Esse fluxo buscava transformar elementos reais de engenharia em códigos de composições previamente associados.

Na abordagem atual, essa etapa foi retirada do fluxo principal do MVP.

O sistema passa a permitir a seleção direta das composições:

```text
Usuário
        ↓
Seleciona uma composição
        ↓
Informa a quantidade
        ↓
ComposicaoQuantificada
```

Essa decisão reduz a complexidade inicial e mantém maior liberdade na composição dos orçamentos.

A resolução automática de elementos reais poderá ser retomada futuramente como um modo assistido, sem necessidade de alterar o pipeline principal de precificação, pois ambos os caminhos poderiam convergir em `ComposicaoQuantificada`.

Possível evolução futura:

```text
Modo livre
────────────────────────────
Seleção direta
        ↓
ComposicaoQuantificada


Modo assistido
────────────────────────────
Elemento real
        ↓
Resolução automática
        ↓
ComposicaoQuantificada
```

---

## Status

| Item | Status |
|---|---|
| `ComposicaoQuantificada` modelada | ✅ |
| Seleção direta de composições | ✅ |
| Validação de quantidade negativa | ✅ |
| Fluxo baseado em `ElementoQuantificavel` | ❌ Retirado do MVP |
| `CatalogoRepository` para resolução automática | ❌ Retirado do MVP |
| Testes do fluxo antigo | ❌ Removidos |
| Questões em aberto | Possível modo assistido futuro |

---

# 2. Catálogo e Identidade dos Itens

## Descrição

O sistema diferencia explicitamente dois conceitos:

```text
Catalogo
```

e:

```text
FontePrecos
```

Esses conceitos possuem responsabilidades diferentes.

O catálogo responde:

> **Onde esta composição ou item é definido e identificado?**

A fonte de preços responde:

> **De onde veio o preço utilizado para precificar este item?**

Conceitualmente:

```text
Catalogo
        ↓
define e identifica
        ↓
ItemCatalogo
```

enquanto:

```text
FontePrecos
        ↓
fornece referência de preço
        ↓
PrecoItemCatalogo
```

Inicialmente, ambos podem corresponder ao SINAPI:

```text
Catálogo: SINAPI
Fonte de preços: SINAPI
```

Entretanto, a separação permite evoluções futuras.

Exemplos:

```text
Catálogo: SINAPI
Fonte de preços: SINAPI
```

```text
Catálogo: PERSONALIZADO
Fonte de preços: BASE PERSONALIZADA
```

ou, potencialmente:

```text
Catálogo: PERSONALIZADO
Fonte de preços: SINAPI
```

desde que os componentes utilizados pela composição personalizada possam ser encontrados na fonte de preços selecionada.

---

## Catalogo

O `Catalogo` representa a origem da definição e identificação de itens e composições.

Sua estrutura atual é:

```text
Catalogo
├── codigo
└── nome
```

Exemplos possíveis:

```text
SINAPI
SICRO
CATALOGO_PERSONALIZADO
```

---

## ItemCatalogo

O `ItemCatalogo` representa um item identificado dentro de um determinado catálogo.

Sua estrutura atual é:

```text
ItemCatalogo
├── codigo
├── descricao
├── tipo
└── catalogo
```

O tipo do item é representado por `TipoItem` e pode ser:

```text
INSUMO
COMPOSICAO
```

Exemplo:

```text
ItemCatalogo
├── codigo = INS-001
├── descricao = Areia Média Lavada
├── tipo = INSUMO
└── catalogo
    ├── codigo = SINAPI
    └── nome = SINAPI
```

A associação entre `ItemCatalogo` e `Catalogo` permite identificar explicitamente a origem de cada item.

Essa distinção é importante para uma futura evolução em que o usuário poderá criar suas próprias composições e trabalhar com catálogos personalizados.

---

## Regra para composições personalizadas

Uma composição personalizada pode ser criada pelo usuário, mas seus componentes precisam ser precificáveis.

Conceitualmente:

```text
Composição personalizada
        ↓
Componentes
        ↓
Cada componente deve possuir preço disponível
        ↓
FontePrecos selecionada
        +
Estado
        +
Competencia
```

Portanto, uma composição só pode ser completamente precificada se todos os seus componentes possuírem preços disponíveis no contexto de precificação utilizado.

Essa regra ainda está em evolução e deverá ser consolidada conforme o suporte a catálogos e fontes de preços personalizados for implementado.

---

## Status

| Item | Status |
|---|---|
| `Catalogo` modelado | ✅ |
| `ItemCatalogo` modelado | ✅ |
| `TipoItem` modelado | ✅ |
| Associação entre item e catálogo | ✅ |
| Suporte efetivo a múltiplos catálogos | ⚠️ Em evolução |
| Catálogos personalizados persistidos | ❌ |
| Criação de composições pelo usuário | ❌ |
| Questões em aberto | Relação entre catálogo, composição selecionada e orçamento |

---

# 3. Busca da Composição

## Descrição

A partir de uma `ComposicaoQuantificada`, o `ComposicaoRepository` é responsável por recuperar a estrutura completa da composição.

A entrada é:

```text
codigo_composicao
        +
Catalogo
```

Conceitualmente:

```text
ComposicaoQuantificada
├── codigo_composicao
└── quantidade

        +

Catalogo

        ↓

ComposicaoRepository.buscar_composicao(
    codigo,
    catalogo
)

        ↓

Composicao
```

O resultado é um objeto `Composicao` contendo:

```text
Composicao
├── codigo
├── descricao
└── items
    ├── ComponenteComposicao
    ├── ComponenteComposicao
    └── ...
```

Cada `ComponenteComposicao` possui:

```text
ComponenteComposicao
├── item
│   └── ItemCatalogo
└── coeficiente
```

O coeficiente representa a quantidade do componente necessária para executar uma unidade da composição.

Exemplo:

```text
COMP-AGUA-003
Tubulação PBA DN 50

├── Tubo PBA DN 50
│   └── coeficiente = 1.05
├── Areia
│   └── coeficiente = 0.10
└── Serviço de escavação
    └── coeficiente = 0.50
```

Ao reconstruir os componentes, o `ComposicaoRepository` associa cada `ItemCatalogo` ao catálogo utilizado na consulta.

---

## Responsabilidade atual do repository

O `ComposicaoRepository` é responsável por:

```text
Receber código + catálogo
        ↓
Consultar a fonte de dados correspondente
        ↓
Localizar a composição
        ↓
Reconstruir seus componentes
        ↓
Associar os itens ao catálogo
        ↓
Retornar um objeto de domínio Composicao
```

O repository não realiza precificação e não calcula custos.

---

## Status

| Item | Status |
|---|---|
| `Composicao` modelada | ✅ |
| `ComponenteComposicao` modelado | ✅ |
| `ItemCatalogo` modelado | ✅ |
| `ComposicaoRepository` implementado | ✅ |
| Consulta por código e catálogo | ✅ |
| Associação do catálogo aos itens | ✅ |
| Testes automatizados | ✅ |
| Totalmente modelado | ⚠️ Em evolução |
| Questões em aberto | Evolução da infraestrutura para múltiplos catálogos |

---

# 4. Competência dos Preços

## Descrição

A competência representa o mês e o ano de referência dos preços utilizados no orçamento.

Como o dia não possui significado para esse conceito do domínio, foi introduzido o Value Object `Competencia`.

Sua estrutura é:

```text
Competencia
├── ano
└── mes
```

Exemplo:

```text
Competencia
├── ano = 2026
└── mes = 6

Representação:
06/2026
```

A competência valida que o mês esteja no intervalo:

```text
1 <= mes <= 12
```

Para integração com fontes de dados e persistência, pode ser convertida para `date` utilizando convencionalmente o primeiro dia do mês:

```text
Competencia(ano=2026, mes=6)
        ↓
2026-06-01
```

O dia `1` não possui significado de negócio. É apenas uma representação técnica da competência mensal.

---

## Status

| Item | Status |
|---|---|
| `Competencia` modelada como Value Object | ✅ |
| Validação do mês | ✅ |
| Conversão para `date` | ✅ |
| Representação mês/ano | ✅ |
| Utilização pelo `PrecoRepository` | ✅ |
| Testes automatizados | ✅ |
| Questões em aberto | Estratégia definitiva de persistência da competência |

---

# 5. Consulta dos Preços

## Descrição

Cada componente de uma composição possui um `ItemCatalogo` associado.

Para precificar esse componente, o `PrecoRepository` consulta o preço correspondente ao contexto desejado.

O preço é representado por:

```text
PrecoItemCatalogo
├── item
├── preco_unitario
├── estado
├── fonte_precos
└── competencia
```

A consulta considera:

```text
ItemCatalogo
        +
Estado
        +
FontePrecos
        +
Competencia
        ↓
PrecoItemCatalogo
```

Exemplo:

```text
Item: Areia Média Lavada
Estado: MG
Fonte de preços: SINAPI
Competência: 06/2026

        ↓

Preço unitário: R$ 42,50
```

---

## FontePrecos

A `FontePrecos` representa a origem dos preços utilizados para precificar os itens.

Sua estrutura atual é:

```text
FontePrecos
├── codigo
└── nome
```

Exemplos possíveis:

```text
SINAPI
SICRO
BASE_CORPORATIVA
COTACAO_INTERNA
BASE_PERSONALIZADA
```

---

## Busca realizada pelo PrecoRepository

O `PrecoRepository` recebe:

```text
item
estado
fonte_precos
competencia
```

e realiza conceitualmente:

```text
FontePrecos
        ↓
Carregamento dos preços
        ↓
Filtro por código do item
        +
Filtro por competência
        ↓
Seleção da coluna correspondente à UF
        ↓
PrecoItemCatalogo
```

A busca atual considera explicitamente:

```text
codigo_do_item
        +
competencia
        +
estado
```

A fonte de preços determina qual conjunto de dados será consultado.

Se nenhum preço for encontrado para o item e a competência informada, a operação deve falhar explicitamente.

Se o estado informado não estiver disponível na fonte de preços, a operação também deve falhar explicitamente.

---

## Regra para preços personalizados

No futuro, o usuário poderá utilizar preços próprios.

Esses preços deverão continuar sendo representados de forma consistente pelo domínio:

```text
PrecoItemCatalogo
├── item
├── preco_unitario
├── estado
├── fonte_precos
└── competencia
```

Portanto, um preço personalizado não deve ser tratado apenas como um valor isolado.

Ele deve estar associado a uma `FontePrecos`, permitindo preservar:

- origem do preço;
- competência;
- contexto geográfico;
- rastreabilidade.

---

## Status

| Item | Status |
|---|---|
| `Estado` modelado | ✅ |
| `FontePrecos` modelada | ✅ |
| `PrecoItemCatalogo` modelado | ✅ |
| `Competencia` modelada | ✅ |
| `PrecoRepository` implementado | ✅ |
| Filtro por código do item | ✅ |
| Filtro por competência | ✅ |
| Seleção do preço por UF | ✅ |
| Validação de preço negativo | ✅ |
| Testes automatizados | ✅ |
| Fontes de preços personalizadas | ❌ |
| Totalmente modelado | ⚠️ Em evolução |
| Questões em aberto | Suporte efetivo a múltiplas fontes e preços personalizados |

---

# 6. Precificação da Composição

## Descrição

Para cada `ComponenteComposicao`, o serviço consulta o preço correspondente e cria um `ComponentePrecificado`.

Sua estrutura é:

```text
ComponentePrecificado
├── componente
│   ├── item
│   └── coeficiente
└── preco_unitario
```

O custo unitário do componente é calculado por:

```text
coeficiente × preco_unitario
```

Exemplo:

```text
Coeficiente = 1.05
Preço unitário = R$ 42,50

Custo unitário do componente = R$ 44,625
```

Todos os componentes precificados são agrupados em uma `ComposicaoPrecificada`.

---

## ComposicaoPrecificada

A estrutura atual é:

```text
ComposicaoPrecificada
├── codigo
├── quantidade
└── componentes
    ├── ComponentePrecificado
    ├── ComponentePrecificado
    └── ...
```

O custo unitário da composição corresponde à soma dos custos unitários dos seus componentes:

```text
custo_unitario =
    Σ componente.custo_unitario
```

O custo total é:

```text
custo_total =
    custo_unitario × quantidade
```

Exemplo:

```text
ComposicaoPrecificada
├── codigo = COMP-AGUA-003
├── quantidade = 150
├── custo_unitario = R$ 80,00
└── custo_total = R$ 12.000,00
```

O estado, a fonte de preços e a competência não são armazenados diretamente em cada `ComposicaoPrecificada`, pois atualmente esse contexto pertence ao orçamento.

Essa decisão deverá ser reavaliada caso o sistema passe a permitir múltiplas fontes de preços ou diferentes competências dentro do mesmo orçamento.

---

## Status

| Item | Status |
|---|---|
| `ComponentePrecificado` modelado | ✅ |
| `ComposicaoPrecificada` modelada | ✅ |
| Cálculo do custo unitário do componente | ✅ |
| Cálculo do custo unitário da composição | ✅ |
| Cálculo do custo total da composição | ✅ |
| Testes automatizados | ✅ |
| Totalmente modelado | ⚠️ Em evolução |
| Questões em aberto | Snapshot histórico e suporte futuro a múltiplos contextos de precificação |

---

# 7. Geração do Orçamento

## Descrição

O `Orcamento` representa o agregado final do processo.

Sua estrutura atual é:

```text
Orcamento
├── id
├── nome
├── descricao
├── estado
├── fonte_precos
├── competencia
└── itens
    ├── ComposicaoPrecificada
    ├── ComposicaoPrecificada
    └── ...
```

O orçamento possui:

- identidade;
- metadados;
- contexto de precificação;
- composições precificadas;
- custo total calculado.

---

## Identidade

Cada orçamento possui um identificador único:

```text
id: str
```

A estratégia atual utiliza UUID para geração de novos identificadores.

---

## Nome

O nome permite a identificação humana do orçamento.

Exemplo:

```text
Infraestrutura — Residencial Belo Horizonte
```

A regra proposta é limitar o nome a 100 caracteres.

---

## Descrição

A descrição fornece contexto adicional e é opcional.

Exemplo:

```text
Orçamento preliminar das redes de água e esgoto do empreendimento.
```

---

## Contexto de precificação

Atualmente, o orçamento define:

```text
Estado
        +
FontePrecos
        +
Competencia
```

Essas informações estabelecem o contexto utilizado para precificar seus componentes.

Exemplo:

```text
Estado: MG
Fonte de preços: SINAPI
Competência: 06/2026
```

O `Catalogo` ainda não está associado diretamente ao agregado `Orcamento`.

Essa decisão permanece em aberto devido à possibilidade futura de:

- um orçamento utilizar composições de diferentes catálogos;
- o usuário criar composições próprias;
- uma composição personalizada utilizar itens precificados por diferentes fontes disponíveis.

A modelagem deverá ser guiada pelos casos de uso concretos definidos para o MVP.

---

## Custo total

O custo total do orçamento corresponde à soma dos custos totais de suas composições precificadas:

```text
custo_total =
    Σ item.custo_total
```

---

## Status

| Item | Status |
|---|---|
| Classe `Orcamento` modelada | ✅ |
| Identidade definida | ✅ |
| Nome e descrição definidos | ✅ |
| Estado associado ao orçamento | ✅ |
| Fonte de preços associada | ✅ |
| Competência associada | ✅ |
| Cálculo de custo total | ✅ |
| `OrcamentoRepository` implementado | ⚠️ Inicial |
| Persistência do identificador | ✅ |
| Persistência completa do agregado | ❌ |
| Reconstrução completa do agregado | ❌ |
| Testes unitários iniciais do repository | ✅ |
| Testes de integração da persistência | ❌ |
| Totalmente modelado | ⚠️ Em evolução |
| Questões em aberto | Catálogos, múltiplas fontes, snapshot histórico e persistência completa |

---

# 8. Service Layer

## Descrição

O fluxo de geração de orçamento é coordenado pela Service Layer.

O principal caso de uso é:

```text
gerar_orcamento(...)
```

Sua responsabilidade atual é orquestrar:

```text
ComposicaoQuantificada[]
        ↓
Para cada composição selecionada:
        ↓
ComposicaoRepository.buscar_composicao(
    codigo,
    catalogo
)
        ↓
Composicao
        ↓
Para cada componente:
        ↓
PrecoRepository.buscar_preco(
    item,
    estado,
    fonte_precos,
    competencia
)
        ↓
PrecoItemCatalogo
        ↓
ComponentePrecificado
        ↓
ComposicaoPrecificada
        ↓
Orcamento
```

A Service Layer coordena o fluxo, enquanto:

- o domínio contém regras e comportamentos;
- os repositories abstraem o acesso aos dados;
- a infraestrutura implementa detalhes de persistência;
- a futura API será responsável pela fronteira HTTP;
- o frontend React será um consumidor da API.

Também existem operações iniciais para:

```text
salvar_orcamento(...)
consultar_orcamento_salvo(...)
```

O gerenciamento da transação ocorre fora do `OrcamentoRepository`, permitindo que o repository se concentre exclusivamente na persistência e recuperação do agregado.

---

## Status

| Item | Status |
|---|---|
| Service Layer introduzida | ✅ |
| `gerar_orcamento` implementado | ✅ |
| Geração direta a partir de composições selecionadas | ✅ |
| Integração com `ComposicaoRepository` | ✅ |
| Integração com `PrecoRepository` | ✅ |
| Filtro por competência | ✅ |
| `salvar_orcamento` implementado inicialmente | ✅ |
| `consultar_orcamento_salvo` implementado inicialmente | ✅ |
| Gerenciamento de commit e rollback | ✅ |
| Persistência completa do agregado | ❌ |
| Testes automatizados | ✅ |
| Questões em aberto | Evolução dos casos de uso e futura introdução de Unit of Work, se necessária |

---

# 9. Persistência

## Descrição

A persistência está sendo introduzida incrementalmente com:

```text
SQLAlchemy
        ↓
SQLite
```

O domínio permanece separado dos modelos ORM.

Atualmente:

```text
Orcamento
        ↓
Conversão domínio → ORM
        ↓
OrcamentoOrm
        ↓
SQLite
```

O `OrcamentoRepository` recebe uma `Session` externamente e não é responsável por:

- criar a sessão;
- realizar `commit`;
- realizar `rollback`;
- encerrar o ciclo de vida da transação.

Essas responsabilidades pertencem à camada que coordena o caso de uso.

---

## Estado atual

A primeira implementação persiste apenas parte do agregado.

O próximo objetivo é evoluir para uma estrutura capaz de representar:

```text
OrcamentoOrm
    1
    │
    N
ComposicaoPrecificadaOrm
    1
    │
    N
ComponentePrecificadoOrm
```

Essa modelagem deverá preservar dados suficientes para que um orçamento histórico não seja silenciosamente recalculado utilizando preços ou informações atuais.

---

## Snapshot histórico

Uma das principais decisões arquiteturais pendentes é definir quais informações deverão ser persistidas como snapshot.

O objetivo é garantir:

```text
Orçamento gerado em 06/2026
        ↓
Catálogos e preços são atualizados
        ↓
Orçamento é consultado posteriormente
        ↓
Resultado histórico permanece inalterado
```

Isso pode exigir a persistência de informações como:

- código e descrição da composição;
- quantidade;
- código e descrição dos componentes;
- coeficientes;
- preços unitários utilizados;
- custos calculados;
- estado;
- fonte de preços;
- competência;
- catálogo de origem, quando aplicável.

A estratégia definitiva ainda será modelada.

---

## Status

| Item | Status |
|---|---|
| SQLAlchemy introduzido | ✅ |
| SQLite configurado | ✅ |
| `DATABASE_URL` via variável de ambiente | ✅ |
| Modelo ORM inicial | ✅ |
| `OrcamentoRepository` inicial | ✅ |
| Separação entre domínio e ORM | ✅ |
| Persistência completa do agregado | ❌ |
| Reconstrução completa do agregado | ❌ |
| Testes de integração | ❌ |
| Migrações com Alembic | ❌ |
| Questões em aberto | Estratégia completa de snapshot histórico |

---

# 10. Cobertura de Testes Atual

## Descrição

Após a simplificação do fluxo e a atualização do domínio, a suíte atual possui:

```text
7 testes passando
```

Distribuídos entre:

```text
test_gerar_orcamento.py
test_precificacao.py
test_salvar_orcamento.py
test_validar_composicao.py
```

Os testes relacionados ao fluxo removido foram excluídos:

```text
test_busca_composicao.py
test_redes.py
```

O estado atual da suíte é:

```text
7 passed
```

A cobertura atual valida comportamentos relacionados a:

- geração do orçamento;
- precificação;
- validações de preço;
- validação de composições;
- conversão inicial entre domínio e ORM para persistência.

---

# Avaliação Geral da Modelagem

## Pontos positivos

- fluxo principal simplificado para seleção direta de composições;
- redução de abstrações que não eram necessárias para o MVP atual;
- `ComposicaoQuantificada` estabelecida como entrada do pipeline de precificação;
- separação entre `Catalogo` e `FontePrecos`;
- `ItemCatalogo` associado explicitamente à sua origem;
- `Competencia` modelada como Value Object;
- consulta de preços considerando item, competência e estado;
- contexto de precificação centralizado no `Orcamento`;
- Repository Pattern utilizado para isolar mecanismos de acesso aos dados;
- Service Layer utilizada para coordenar os casos de uso;
- domínio independente de SQLAlchemy, FastAPI e React;
- persistência introduzida sem acoplar modelos ORM ao domínio;
- testes automatizados alinhados ao fluxo atual;
- arquitetura preparada para evolução incremental.

---

## Pontos de atenção

### Catálogo da composição

Atualmente, o serviço recebe um catálogo utilizado para localizar as composições.

Entretanto, o sistema deverá futuramente permitir composições próprias criadas pelo usuário.

Permanece em aberto decidir se:

```text
Opção A
Um orçamento utiliza apenas um catálogo
```

ou:

```text
Opção B
Cada composição selecionada identifica seu próprio catálogo
```

A decisão deverá considerar os casos de uso reais do MVP.

---

### Fonte de preços

Atualmente, o orçamento possui uma única `FontePrecos`.

Entretanto, composições personalizadas podem exigir preços próprios.

Permanece em aberto decidir se:

```text
Opção A
Um orçamento utiliza apenas uma fonte de preços
```

ou:

```text
Opção B
Diferentes itens ou composições podem utilizar diferentes fontes
```

Essa decisão impactará:

- o agregado `Orcamento`;
- `ComposicaoPrecificada`;
- `ComponentePrecificado`;
- persistência;
- snapshot histórico;
- API;
- experiência do usuário no frontend.

A complexidade de múltiplas fontes não deve ser introduzida antes de existir um caso de uso concreto que a justifique.

---

### Identidade dos itens entre catálogos

O código isolado pode não ser suficiente para identificar globalmente um item caso diferentes catálogos utilizem o mesmo código.

Exemplo:

```text
SINAPI
└── código = 12345

CATALOGO_PERSONALIZADO
└── código = 12345
```

Pode ser necessário considerar a identidade composta:

```text
catalogo + codigo
```

Essa questão deverá ser considerada na persistência e nas consultas.

---

### Valores monetários

`PrecoItemCatalogo` utiliza `Decimal`.

É recomendável garantir que todos os valores monetários do domínio também utilizem `Decimal`, evitando misturas com `float` e possíveis inconsistências de precisão.

---

### Acoplamento entre domínio e nomes físicos das fontes de dados

Atualmente, `catalogo.nome` e `fonte_precos.nome` podem ser utilizados diretamente para localizar arquivos.

Isso cria potencial acoplamento entre:

```text
Conceito de domínio
        ↓
Nome físico do arquivo
```

Futuramente, a infraestrutura poderá introduzir um mapeamento explícito:

```text
SINAPI
        ↓
Configuração de infraestrutura
        ↓
arquivo físico / tabela / banco / API
```

Assim, o domínio não precisará conhecer detalhes físicos de armazenamento.

---

### Snapshot histórico

A principal questão arquitetural pendente continua sendo definir quais informações precisam ser persistidas para preservar fielmente um orçamento histórico.

O objetivo é garantir que:

```text
Orçamento gerado em 06/2026
        ↓
Preços, catálogos e descrições mudam
        ↓
Orçamento consultado posteriormente
        ↓
Mantém exatamente o resultado histórico original
```

---

# Próximas Etapas

A evolução imediata está concentrada na consolidação do domínio e na persistência completa do agregado `Orcamento`.

Sequência recomendada:

```text
1. Consolidar a relação entre Catalogo, ComposicaoQuantificada e Orcamento
        ↓
2. Consolidar a regra de FontePrecos para o MVP
        ↓
3. Definir a estratégia de snapshot histórico
        ↓
4. Modelar a persistência completa do Orcamento
        ↓
5. Modelar ComposicaoPrecificadaOrm
        ↓
6. Modelar ComponentePrecificadoOrm
        ↓
7. Persistir o agregado completo
        ↓
8. Reconstruir o domínio a partir do ORM
        ↓
9. Implementar testes de integração
        ↓
10. Introduzir migrações com Alembic
```

Após a fundação da persistência:

```text
Persistência completa
        ↓
CRUD dos recursos necessários
        ↓
Relatórios e exportação
        ↓
FastAPI + Pydantic
        ↓
Integração com React
        ↓
MVP e Deploy
```

---

# Fluxo Consolidado Atual

```text
Usuário seleciona composições e quantidades
        ↓
ComposicaoQuantificada[]
        ↓
gerar_orcamento(...)
        ↓
Para cada composição:
        ↓
ComposicaoRepository
├── código
└── catálogo
        ↓
Composicao
        ↓
Para cada componente:
        ↓
PrecoRepository
├── item
├── estado
├── fonte de preços
└── competência
        ↓
PrecoItemCatalogo
        ↓
ComponentePrecificado
        ↓
ComposicaoPrecificada
        ↓
Orcamento
├── id
├── nome
├── descrição
├── estado
├── fonte de preços
├── competência
├── itens
└── custo total
```