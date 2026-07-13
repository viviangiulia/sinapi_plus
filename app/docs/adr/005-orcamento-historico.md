# ADR-005 — Estratégia de snapshot histórico e recálculo de orçamentos

## Status

Aceita.

## Contexto

Um orçamento é calculado a partir de dados provenientes de catálogos de referência, incluindo composições, componentes, coeficientes e preços.

Esses dados podem mudar ao longo do tempo. Uma composição pode ter sua descrição alterada, seus componentes modificados, seus coeficientes atualizados ou até mesmo deixar de existir no catálogo. Da mesma forma, os preços dos componentes podem variar entre diferentes competências.

Por esse motivo, recuperar um orçamento antigo consultando os catálogos atuais poderia alterar silenciosamente sua memória de cálculo e seus resultados financeiros.

É necessário distinguir claramente duas operações:

1. recuperar um orçamento histórico;
2. recalcular um orçamento utilizando os dados atuais dos catálogos.

## Decisão

### 1. Recuperação de orçamento histórico

Um orçamento recuperado representa um snapshot histórico dos dados persistidos no momento em que foi gerado.

A recuperação deve utilizar exclusivamente os dados armazenados no banco de dados para o orçamento, sem substituir silenciosamente valores históricos por dados provenientes dos catálogos atuais.

O orçamento recuperado deve preservar os dados de negócio e resultados financeiros originalmente persistidos.

### 2. Dados persistidos do orçamento

O orçamento deve persistir:

* identificador;
* nome;
* descrição;
* estado;
* fonte de preços;
* competência;
* composições precificadas que constituíam o orçamento.

### 3. Snapshot de uma composição precificada

Para cada ocorrência de uma composição dentro do orçamento, devem ser persistidos:

* código da composição;
* descrição;
* unidade;
* categoria;
* quantidade;
* custo unitário calculado;
* custo total calculado.

Cada ocorrência possui identidade técnica própria no banco de dados.

O código da composição não é único dentro de um orçamento, pois a mesma composição pode ser utilizada múltiplas vezes, inclusive em categorias diferentes.

### 4. Snapshot dos componentes da composição

Para cada componente utilizado na precificação de uma composição, devem ser persistidos:

* código do componente;
* descrição;
* tipo;
* unidade;
* coeficiente utilizado;
* custo unitário utilizado.

Descrições e coeficientes fazem parte do snapshot histórico, pois podem ser alterados posteriormente nos catálogos de referência.

A consulta de um orçamento histórico não deve substituir esses valores pelos valores atuais dos catálogos.

### 5. Recálculo com dados atuais

O recálculo é uma operação explícita e distinta da recuperação de um orçamento histórico.

Para recalcular um orçamento, devem ser reaproveitados do orçamento original:

* código da composição;
* quantidade;
* categoria.

A partir do código da composição, o sistema deve consultar o catálogo atual e executar novamente o fluxo normal de precificação utilizando:

* a versão atual da composição;
* os componentes atuais da composição;
* os coeficientes atuais;
* os preços atuais disponíveis.

Portanto, o recálculo não utiliza os componentes, coeficientes nem preços históricos para produzir o novo resultado. Esses dados permanecem preservados apenas como parte do snapshot original.

Uma composição só poderá ser recalculada caso seu código ainda exista no catálogo atual.

### 6. Separação entre dados históricos e catálogos atuais

Os dados históricos persistidos no orçamento são independentes do estado atual dos catálogos.

A recuperação histórica segue o fluxo:

```text
Orçamento persistido
        ↓
Snapshot armazenado no banco
        ↓
Reconstrução do orçamento histórico
```

O recálculo segue um fluxo diferente:

```text
Orçamento histórico
        ↓
Código + quantidade + categoria
        ↓
Consulta ao catálogo atual
        ↓
Composição e componentes atuais
        ↓
Coeficientes e preços atuais
        ↓
Nova precificação
```

Nenhuma consulta aos catálogos atuais deve modificar silenciosamente a representação de um orçamento histórico.

## Modelo de persistência adotado

A estrutura conceitual de persistência é:

```text
OrcamentoOrm
    │
    └── ComposicaoPrecificadaOrm
                │
                └── ComponenteComposicaoPersistidoOrm
```

### `OrcamentoOrm`

Representa o orçamento salvo e possui relacionamento de um para muitos com suas composições precificadas.

### `ComposicaoPrecificadaOrm`

Representa uma ocorrência específica de uma composição dentro de um orçamento.

Persiste:

```text
id
orcamento_id
codigo
descricao
unidade
categoria
quantidade
custo_unitario
custo_total
```

### `ComponenteComposicaoPersistidoOrm`

Representa o snapshot de um componente utilizado na memória de cálculo de uma composição precificada.

Persiste:

```text
id
composicao_precificada_id
codigo
descricao
tipo
unidade
coeficiente
custo_unitario
```

## Consequências

### Consequências positivas

* Orçamentos históricos permanecem estáveis mesmo após alterações nos catálogos.
* A memória de cálculo original pode ser consultada posteriormente.
* Alterações de descrições, componentes, coeficientes ou preços não modificam silenciosamente orçamentos já salvos.
* O recálculo com dados atuais possui semântica explícita e separada da recuperação histórica.
* A mesma composição pode ocorrer múltiplas vezes dentro de um orçamento.

### Consequências negativas

* Existe desnormalização intencional de dados, pois descrições, unidades e outras informações disponíveis nos catálogos também são armazenadas no snapshot.
* O volume de dados persistidos é maior.
* Dados derivados, como custos totais, podem ser armazenados juntamente com os dados que permitiriam recalculá-los.
* A operação de recálculo precisa tratar explicitamente composições que deixaram de existir no catálogo atual.

## Invariantes adotadas

1. Recuperar um orçamento histórico nunca deve alterar silenciosamente seus valores com base nos catálogos atuais.
2. Um orçamento histórico deve ser reconstruído a partir de seu snapshot persistido.
3. O código de uma composição não é único dentro de um orçamento.
4. Descrições, unidades, coeficientes e preços utilizados fazem parte do histórico.
5. O recálculo é uma operação explícita.
6. O recálculo reaproveita código, quantidade e categoria da composição original.
7. O recálculo utiliza a composição, os componentes, os coeficientes e os preços atualmente disponíveis nos catálogos.
8. O snapshot histórico original permanece preservado independentemente de futuras operações de recálculo.
