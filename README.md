# SINAPI+

## Simulador de Custos de Infraestrutura

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

O **SINAPI+** é uma aplicação para geração e análise de orçamentos de infraestrutura da construção civil, utilizando composições e preços regionalizados de referência do **SINAPI — Sistema Nacional de Pesquisa de Custos e Índices da Construção Civil**.

Além de seu objetivo funcional, o projeto é desenvolvido como um **projeto de portfólio e laboratório de arquitetura de software**, explorando modelagem de domínio, separação de responsabilidades, padrões de projeto, persistência, APIs e desenvolvimento full stack.

> **Status do projeto:** o SINAPI+ está atualmente passando por uma reconstrução arquitetural e pela migração de sua interface original em Streamlit para uma arquitetura desacoplada, com backend Python e frontend React.

---

## 🔍 Sobre o projeto

O orçamento de infraestrutura envolve a transformação de elementos reais de uma obra — como tubulações, hidrômetros, poços de visita e outros serviços — em composições de custos formadas por materiais, mão de obra e equipamentos.

O SINAPI+ busca simplificar esse processo por meio de um fluxo estruturado:

```text
Dados de entrada
        ↓
ElementoQuantificavel
        ↓
CatalogoRepository
        ↓
ComposicaoQuantificada
        ↓
ComposicaoRepository
        ↓
Composicao
        ↓
PrecoRepository
        ↓
ComponentePrecificado
        ↓
ComposicaoPrecificada
        ↓
Orcamento
```

A aplicação associa as características técnicas de cada elemento a uma composição correspondente, consulta seus componentes, aplica preços regionalizados e consolida os resultados em um orçamento.

Um dos principais objetivos arquiteturais é manter as **regras de negócio independentes da interface, do banco de dados e dos frameworks utilizados**, permitindo que o domínio evolua sem ficar acoplado à infraestrutura.

---

## 🎯 Objetivos técnicos

O projeto também funciona como um ambiente prático para estudo e aplicação de conceitos de engenharia de software:

- Domain Modeling;
- Clean Code;
- princípios SOLID;
- separação entre domínio, aplicação e infraestrutura;
- Repository Pattern;
- Service Layer;
- Dependency Inversion Principle;
- Design Patterns aplicados a problemas reais;
- testes unitários e de integração;
- persistência com SQLAlchemy;
- API REST com FastAPI e Pydantic;
- frontend em React;
- AIDD — AI-Driven Development — como apoio ao desenvolvimento do frontend;
- documentação de decisões arquiteturais através de ADRs.

As decisões são introduzidas incrementalmente conforme surgem necessidades reais no domínio, evitando adicionar abstrações ou padrões sem uma responsabilidade concreta.

---

## 🏗️ Arquitetura

A arquitetura pretendida para a nova versão do SINAPI+ é:

```text
┌──────────────────────────┐
│          React           │
│        Frontend          │
└────────────┬─────────────┘
             │ HTTP / JSON
             ▼
┌──────────────────────────┐
│   FastAPI + Pydantic     │
│      API / Schemas       │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│     Application Layer    │
│  Service Layer / Use     │
│          Cases           │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│       Domain Model       │
│   Regras e entidades     │
│       de negócio         │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│       Repositories       │
│  Abstração de acesso a   │
│          dados           │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│       SQLAlchemy         │
│      Persistência        │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│      Banco de Dados      │
└──────────────────────────┘
```

Uma das principais diretrizes arquiteturais do projeto é que o **domínio não dependa da API, do ORM ou da interface gráfica**.

A direção das dependências busca manter as regras de negócio no centro da aplicação:

```text
Interface ──────────┐
                    ▼
API ──────► Application Layer ──────► Domain Model
                    │
                    ▼
               Repositories
                    │
                    ▼
               Infrastructure
```

---

## 📊 Status atual

### ✅ Implementado

- Modelagem inicial do domínio de orçamentos;
- representação de elementos quantificáveis e suas especificações;
- modelagem de redes, trechos e tubulações;
- geração de elementos quantificáveis a partir de objetos do domínio;
- associação entre elementos e códigos de composição através de catálogo;
- consulta das composições e seus componentes;
- precificação regionalizada dos componentes;
- geração do agregado `Orcamento`;
- Repository Pattern para acesso às diferentes fontes de dados;
- Service Layer para orquestração dos casos de uso;
- persistência inicial com SQLAlchemy e SQLite;
- separação entre modelos de domínio e modelos ORM;
- `OrcamentoRepository` para persistência e consulta inicial de orçamentos;
- configuração da conexão com o banco através de variáveis de ambiente;
- testes automatizados do domínio, repositories e serviços;
- documentação de decisões arquiteturais através de ADRs.

### 🚧 Em desenvolvimento

- persistência completa do agregado `Orcamento`;
- modelagem ORM das composições precificadas;
- modelagem ORM dos componentes precificados;
- reconstrução completa de um orçamento a partir da persistência;
- testes de integração da camada de persistência;
- frontend em React, desenvolvido inicialmente com dados mockados.

### 🗺️ Planejado

- estratégia completa de snapshot histórico dos orçamentos;
- migrações de banco de dados;
- relatórios e exportações;
- API REST com FastAPI;
- contratos de entrada e saída com Pydantic;
- integração entre React e FastAPI;
- consulta de orçamentos salvos pelo frontend;
- deploy do MVP;
- pipeline básico de integração contínua.

---

## 🚀 Funcionalidades

### Geração de orçamentos

A aplicação permite transformar elementos de infraestrutura em composições precificadas através do seguinte processo:

1. Recebimento dos elementos quantificáveis;
2. identificação da composição correspondente através do catálogo;
3. consulta dos dados e componentes da composição;
4. consulta dos preços regionalizados;
5. precificação de cada componente;
6. consolidação em uma composição precificada;
7. geração do orçamento completo.

### Regionalização de preços

Os preços são associados ao estado utilizado como referência para o orçamento, permitindo trabalhar com diferentes contextos regionais brasileiros.

### Categorias atualmente modeladas

#### Água potável

- tubulações;
- hidrômetros;
- outros elementos relacionados à infraestrutura de abastecimento.

#### Esgoto sanitário

- tubulações;
- poços de visita;
- outros elementos relacionados à infraestrutura sanitária.

Categorias como drenagem, pavimentação e energia poderão ser incorporadas futuramente conforme a evolução do domínio.

---

## 🛠️ Stack tecnológica

| Tecnologia | Finalidade | Status |
|---|---|---|
| **Python** | Linguagem principal do backend e domínio | Implementado |
| **Pandas** | Consulta e transformação das bases de referência atuais | Implementado |
| **OpenPyXL** | Leitura das bases em Excel | Implementado |
| **SQLAlchemy** | ORM e persistência | Implementado |
| **SQLite** | Banco de dados durante o desenvolvimento inicial | Implementado |
| **Pytest** | Testes automatizados | Implementado |
| **React** | Novo frontend da aplicação | Em desenvolvimento |
| **JavaScript** | Linguagem do frontend | Em desenvolvimento |
| **FastAPI** | API REST | Planejado |
| **Pydantic** | Contratos e validação na fronteira da API | Planejado |
| **Alembic** | Migrações do banco de dados | Planejado |

---

## 🤖 Desenvolvimento do frontend com AIDD

O novo frontend em React é desenvolvido com apoio de uma abordagem de **AI-Driven Development (AIDD)**.

A IA é utilizada como ferramenta de apoio para acelerar atividades como:

- exploração de alternativas visuais;
- geração inicial de componentes;
- refinamento da interface;
- identificação de padrões reutilizáveis;
- apoio à implementação e refatoração.

O uso de AIDD não substitui as decisões arquiteturais do projeto. O frontend continua sendo desenvolvido considerando separação de responsabilidades, componentes reutilizáveis e uma fronteira explícita entre interface e backend.

Inicialmente, o frontend pode operar com dados mockados. Posteriormente, esses mocks serão substituídos progressivamente pelos contratos reais da API FastAPI.

---

## 🧪 Testes

O projeto utiliza `pytest` para validar o comportamento do domínio, dos repositories e dos casos de uso.

Os testes buscam verificar regras e comportamentos observáveis, evitando acoplamento excessivo aos detalhes internos de implementação.

Para executar a suíte:

```bash
python -m pytest
```

Entre os cenários atualmente cobertos estão:

- validação de objetos do domínio;
- geração de elementos quantificáveis;
- busca de composições;
- precificação;
- geração de orçamento;
- conversão inicial entre objetos de domínio e modelos ORM.

A evolução planejada inclui testes de integração para validar o ciclo completo:

```text
Criar Orcamento
        ↓
Persistir
        ↓
Commit
        ↓
Recuperar
        ↓
Reconstruir agregado
        ↓
Comparar resultado
```

---

## 🗺️ Roadmap

O desenvolvimento do SINAPI+ está organizado em cinco milestones:

### M1 — Fundação da Persistência

Persistência e reconstrução completa do agregado `Orcamento`.

Principais objetivos:

- definir a estratégia de snapshot histórico;
- persistir as composições precificadas;
- persistir os componentes precificados;
- reconstruir o agregado completo;
- implementar testes de integração;
- introduzir migrações do banco de dados.

### M2 — Relatórios e Exportação

Definição e implementação dos primeiros relatórios disponibilizados pela aplicação.

Principais objetivos:

- definir os requisitos dos relatórios;
- selecionar os relatórios necessários para o MVP;
- implementar a primeira exportação.

### M3 — Fundação da API

Exposição dos casos de uso através de FastAPI e contratos Pydantic.

Principais objetivos:

- definir os contratos HTTP;
- estruturar a aplicação FastAPI;
- expor o caso de uso de geração de orçamento;
- disponibilizar operações de persistência e consulta.

### M4 — Frontend React e Integração

Desenvolvimento da experiência de usuário e integração progressiva com o backend.

Principais objetivos:

- desenvolver a interface inicialmente com dados mockados;
- implementar formulários de entrada;
- apresentar os resultados do orçamento;
- tratar estados de carregamento, erro e ausência de dados;
- substituir progressivamente os mocks pela API real.

### M5 — MVP e Deploy

Preparação da primeira versão completa e publicamente demonstrável.

Principais objetivos:

- preparar frontend e backend para produção;
- definir a estratégia de banco de dados de produção;
- configurar variáveis de ambiente;
- documentar a execução da aplicação;
- implementar integração contínua;
- realizar o deploy do fluxo principal.

O roadmap detalhado, as prioridades, os critérios de aceite e o andamento das implementações são acompanhados através do GitHub Project associado ao repositório.

---

## 📝 Decisões arquiteturais

As principais decisões técnicas do projeto são documentadas através de **Architecture Decision Records (ADRs)**.

Entre os temas explorados estão:

- modelagem do domínio;
- separação entre regras de negócio e infraestrutura;
- utilização do Repository Pattern;
- Service Layer e orquestração de casos de uso;
- persistência e reconstrução de agregados;
- evolução das fontes de dados;
- estratégia de snapshot histórico dos orçamentos.

Essa documentação busca preservar não apenas **o que foi implementado**, mas também **por que determinadas decisões foram tomadas**.

---

## 📁 Estrutura do projeto

A estrutura atual do backend reflete a evolução incremental do SINAPI+, desde sua primeira versão em Streamlit até a nova arquitetura orientada ao domínio.

```text
sinapi_plus/
├── app/
│   ├── api/                       # Camada da API e futuros endpoints FastAPI
│   ├── configs/                   # Configurações da aplicação
│   ├── docs/                      # Documentação técnica e ADRs
│   ├── excel_files/               # Bases de referência utilizadas atualmente
│   ├── images/                    # Recursos visuais da aplicação legada
│   ├── infrastructure/            # Persistência, ORM e configuração do banco
│   ├── pages/                     # Páginas da interface Streamlit legada
│   ├── repositories/              # Acesso e abstração das fontes de dados
│   ├── streamlit/                 # Componentes relacionados à aplicação legada
│   ├── study/                     # Experimentos e exercícios de estudo
│   ├── tests/                     # Testes automatizados
│   │
│   ├── app_state.py               # Gerenciamento de estado da aplicação legada
│   ├── create_database.py         # Inicialização do banco de dados
│   ├── data_loading.py            # Carregamento das bases de referência
│   ├── exceptions.py              # Exceções específicas da aplicação
│   ├── main.py                    # Ponto de entrada da aplicação legada
│   ├── models.py                  # Modelo de domínio
│   ├── orcamento_service.py       # Service Layer e casos de uso de orçamento
│   ├── ProcessarComposicao.py     # Implementação legada do motor de cálculo
│   └── utils.py                   # Funções auxiliares
│
├── requirements.txt
├── .env.example
└── README.md
```

O novo backend está sendo desenvolvido incrementalmente, preservando temporariamente partes da implementação anterior em Streamlit para referência e comparação durante a migração.

A arquitetura atual separa conceitualmente as seguintes responsabilidades:

```text
models.py
    ↓
Modelo de domínio e regras de negócio

orcamento_service.py
    ↓
Service Layer e orquestração dos casos de uso

repositories/
    ↓
Abstração do acesso às fontes de dados

infrastructure/
    ↓
SQLAlchemy, modelos ORM e configuração do banco de dados

api/
    ↓
Futura fronteira HTTP com FastAPI e Pydantic

tests/
    ↓
Testes do domínio, repositories, serviços e persistência
```

A organização física do projeto poderá evoluir conforme o domínio e a aplicação crescerem. Por enquanto, o modelo de domínio permanece concentrado em `models.py`, evitando uma fragmentação prematura em múltiplos módulos sem necessidade concreta.

---

## 🔧 Instalação e execução

### Pré-requisitos

- Python compatível com a versão definida pelo projeto;
- Git.

### 1. Clone o repositório

```bash
git clone https://github.com/viviangiulia/sinapi_plus.git
```

### 2. Acesse o diretório

```bash
cd sinapi_plus
```

### 3. Crie um ambiente virtual

```bash
python -m venv venv
```

### 4. Ative o ambiente virtual

#### Windows

```bash
venv\Scripts\activate
```

#### Linux ou macOS

```bash
source venv/bin/activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Configure as variáveis de ambiente

Crie um arquivo `.env` a partir do `.env.example` disponibilizado no projeto.

Linux ou macOS:

```bash
cp .env.example .env
```

No Windows, o arquivo também pode ser copiado manualmente.

### 7. Execute os testes

```bash
python -m pytest
```

> Os comandos de execução da API FastAPI e do novo frontend React serão adicionados conforme essas etapas forem integradas à versão principal do projeto.

---

## 📈 Fontes de dados

O projeto utiliza dados públicos de referência do **SINAPI — Sistema Nacional de Pesquisa de Custos e Índices da Construção Civil**.

Os dados incluem informações relacionadas a:

- composições;
- insumos;
- coeficientes;
- preços regionalizados.

As fontes de dados atuais ainda utilizam arquivos Excel em parte da infraestrutura. A arquitetura com repositories busca isolar essa decisão das regras de negócio, permitindo a evolução futura das fontes de dados sem modificar o domínio.

---

## 🕰️ Histórico da aplicação

A primeira versão funcional do SINAPI+ foi desenvolvida com Streamlit e serviu como prova de conceito para validar o problema e o fluxo de geração de orçamentos.

A aplicação está sendo reconstruída para uma arquitetura desacoplada:

```text
Versão inicial
Streamlit + Pandas + Excel
            ↓
Nova arquitetura
React + FastAPI + Domain Model + Repositories + SQLAlchemy
```

A versão anterior permanece como parte do histórico de evolução do projeto.

---

## 🤝 Contribuição

O projeto está atualmente em desenvolvimento ativo e é utilizado principalmente para fins de estudo, portfólio e experimentação arquitetural.

Sugestões e discussões técnicas são bem-vindas, especialmente relacionadas a:

- modelagem de domínio;
- arquitetura de software;
- construção civil e orçamentação;
- persistência;
- APIs;
- testes;
- experiência de usuário.

---

## 📄 Licença e uso dos dados

Este projeto é desenvolvido para fins educacionais e de portfólio.

Os dados públicos utilizados como referência permanecem sujeitos às condições e regras aplicáveis às respectivas fontes oficiais.

---

## 👩‍💻 Autora

**Vivian Giulia Fernandes**

Engenheira Civil formada pela Universidade Federal de Minas Gerais, desenvolvendo soluções de software para problemas reais da construção civil e aprofundando conhecimentos em desenvolvimento backend, arquitetura de software e Python.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vivian-fernandes-099b34149/)

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/viviangiulia)

---

## ⚠️ Disclaimer

Este projeto não possui vínculo oficial com a Caixa Econômica Federal ou com os responsáveis oficiais pelo SINAPI.

Os dados de referência são utilizados conforme sua disponibilização pública para fins educacionais, de estudo e de demonstração técnica.