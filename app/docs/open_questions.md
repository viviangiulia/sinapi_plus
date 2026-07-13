# Open Questions — Snapshot histórico e recálculo de orçamentos

As decisões centrais sobre persistência histórica e recálculo já foram definidas. Permanecem abertas as seguintes questões de comportamento e implementação.

## 1. O que acontece quando uma composição não existe mais no catálogo atual?

Ao recalcular um orçamento, uma ou mais composições históricas podem não existir no catálogo atual.

É necessário definir se a operação deve:

* falhar integralmente e impedir todo o recálculo;
* recalcular as composições disponíveis e reportar as indisponíveis;
* permitir ao usuário substituir manualmente uma composição inexistente.

### Decisão pendente

Definir a política de tratamento para composições históricas ausentes no catálogo atual.

---

## 2. O recálculo cria um novo orçamento ou uma nova versão?

O snapshot original deve permanecer imutável, mas ainda é necessário definir a identidade do resultado do recálculo.

Possibilidades:

* criar um orçamento completamente novo e independente;
* criar um novo orçamento mantendo uma referência ao orçamento de origem;
* implementar futuramente um conceito explícito de versionamento de orçamento.

### Decisão pendente

Definir se o resultado do recálculo é independente ou mantém rastreabilidade formal com o orçamento histórico de origem.

---

## 3. Como tratar um recálculo parcialmente possível?

Um orçamento pode conter diversas composições, das quais apenas algumas ainda existem no catálogo atual.

É necessário definir se o recálculo é uma operação atômica:

```text
Todas as composições podem ser recalculadas
    → sucesso

Pelo menos uma composição não pode ser recalculada
    → falha completa
```

ou parcial:

```text
Composições disponíveis
    → recalculadas

Composições indisponíveis
    → reportadas como erro ou pendência
```

### Decisão pendente

Definir se o recálculo exige sucesso integral ou admite resultado parcial.

---

## 4. Como deve ser apresentada a diferença entre o histórico e o recálculo?

Como o orçamento histórico e o resultado recalculado podem possuir diferenças de preço e até de estrutura das composições, pode ser útil oferecer uma comparação futura.

Exemplos:

* variação do custo total;
* variação por categoria;
* variação por composição;
* componentes adicionados ou removidos;
* alterações de coeficientes.

### Decisão pendente

Definir se a comparação entre snapshot histórico e orçamento recalculado faz parte do escopo futuro do produto.

---

## 5. Qual deve ser a política de imutabilidade de um orçamento salvo?

A recuperação histórica deve reproduzir o snapshot persistido, mas ainda é necessário definir quais campos podem ser editados depois do salvamento.

Por exemplo:

* nome;
* descrição;
* categoria;
* quantidade;
* composições;
* valores calculados.

Uma possível política é permitir alterações apenas em metadados, como nome e descrição, mantendo imutáveis os dados financeiros e a memória de cálculo.

### Decisão pendente

Definir quais campos de um orçamento salvo podem ser alterados sem gerar um novo snapshot.

---

## 6. Qual precisão e política de arredondamento devem ser utilizadas?

O modelo de persistência utiliza valores decimais para quantidades, coeficientes e custos, mas ainda é necessário formalizar:

* número de casas decimais para quantidades;
* número de casas decimais para coeficientes;
* número de casas decimais para preços unitários;
* número de casas decimais para custos totais;
* regra de arredondamento utilizada pelo domínio.

### Decisão pendente

Formalizar a precisão decimal e as regras de arredondamento para garantir consistência entre cálculo, persistência e recuperação.
