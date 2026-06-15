# Glossário do Domínio

Este documento centraliza a terminologia técnica e as regras de negócio do sistema, servindo como fonte única de verdade para desenvolvedores e especialistas do domínio.

---

## 1. Contexto de Orçamentação e Custos
### Orçamento

**Descrição:**
Resultado final consolidado do projeto. Reúne todos os itens orçamentários calculados, suas quantidades e respectivos custos.

---

### Item Orçamentário

**Descrição:**
Representa uma linha do orçamento composta por uma quantidade e uma composição associada.

**Observação:**
Um item orçamentário não representa necessariamente um elemento físico do empreendimento. Ele representa a forma como esse elemento é quantificado e precificado.

---

### Custo Unitário

**Descrição:**
Valor monetário associado a uma composição para uma determinada localidade.

---

### Estado

**Descrição:**
Unidade federativa utilizada para determinar a tabela de preços regionais aplicada ao orçamento.

*Candidato a Value Object.*

---

## 2. Contexto de Engenharia e Composições
### Composição (CPU)

**Descrição:**
Serviço de engenharia identificado por um código único.

Uma composição define os recursos necessários para executar uma unidade de serviço.

**Exemplos:**

    Rede de água em PVC DN 50 mm
    Ligação predial de água
    Poço de visita com profundidade específica

*Candidata a Entity.*

---

### Índice (Coeficiente de Consumo)

**Descrição:**
Fator que determina a quantidade necessária de um material ou subcomposição para execução de uma unidade da composição principal.

---

## 3. Contexto de Elementos de Infraestrutura
### Rede

**Descrição:**
Conjunto de trechos que compõem uma infraestrutura linear.

A principal responsabilidade da Rede é consolidar os quantitativos de seus trechos por Tubulação para posterior geração dos itens orçamentários.

**Exemplos:**

    Rede de água
    Rede de esgoto
    Rede de drenagem

*Possível Entity.*

---

### Trecho de Rede

**Descrição:**
Segmento individual de uma Rede.

Cada trecho possui:

- Identificador único
- Tubulação associada
- Comprimento

Um trecho não pode possuir comprimento negativo.
**Exemplos de atributos:**

    Comprimento
    Material
    Diâmetro

*Possível Entity.*

---

## Tubulação

**Descrição:**
Representa uma especificação técnica de tubulação.

É definida pela combinação de:

    - Material
    - Diâmetro

Duas tubulações são consideradas equivalentes quando possuem o mesmo material e diâmetro.

**Exemplos:**

    PVC DN 50
    PVC DN 75
    DEFOFO DN 150

*Forte candidato a Value Object.*

---

## 4. Contexto de Elementos Quantificáveis
### Elemento Quantificável

**Descrição:**
Elemento físico do empreendimento cuja quantificação gera itens orçamentários.

Pode possuir ou não especificações técnicas adicionais.

**Exemplos:**

    Hidrômetro
    Ligação predial
    Poço de visita
    Boca de lobo
    Hidrômetro

**Descrição:**
Elemento quantificado por unidade.

Sua quantificação normalmente gera diretamente um item orçamentário associado a uma composição específica.

---

**Ligação Predial**

**Descrição:**
Elemento quantificado por unidade.

Sua quantificação normalmente gera diretamente um item orçamentário associado a uma composição específica.

---

**Poço de Visita**

**Descrição:**
Elemento quantificável cuja composição pode variar conforme características técnicas.

**Exemplo:**

    Profundidade

---

**Boca de Lobo**

**Descrição:**
Elemento quantificável cuja composição pode variar conforme características técnicas.

**Exemplos:**

    Com grelha
    Sem grelha

---

## 5. Conceitos Técnicos Compartilhados
### Material

**Descrição:**
Material utilizado na execução de um elemento de infraestrutura.

**Exemplos:**

    PVC
    PBA
    DEFOFO
    Concreto

*Possível Enum de domínio.*

Atualmente faz parte da identidade de uma Tubulação.
---

### Diâmetro

**Descrição:**
Possível Value Object ou Enum de domínio.

Atualmente faz parte da identidade de uma Tubulação.

---

### Comprimento

**Descrição:**
Representa a extensão linear de um Trecho de Rede.

Não pode assumir valores negativos.

*Possível Value Object em futuras evoluções do domínio.*

---

### Profundidade

*Descrição:*
Dimensão vertical utilizada para especificação de determinados elementos de infraestrutura.

*Forte candidato a Value Object.*

---

**Conceitos ainda em investigação**

Os conceitos abaixo ainda precisam de validação durante a modelagem:

| Conceito     | Hipótese Atual                   |
| ------------ | -------------------------------- |
| Rede         | Entity                           |
| TrechoRede   | Entity                           |
| Tubulação    | Value Object                     |
| Composição   | Entity                           |
| Estado       | Value Object                     |
| Material     | Parte da identidade de Tubulação |
| Diâmetro     | Parte da identidade de Tubulação |
| Comprimento  | Possível Value Object            |
| Profundidade | Possível Value Object            |
