
# VeículosLLM

Teste prático contendo uma arquitetura MCP utilizando uma LLM da OLLAMA

O sistema recebe um input do usuário e realiza uma query em um banco SQLite que é iniciado ao iniciar a aplicação, com 
isso você terá o retorno em forma de tabela no CMD o output com base nos dados que foram solicitado pelo usuário, o
sistema continua ativo até que você digite para sair

``` 
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── docker-compose.yml
├── main.py
├── requirements.txt
├── scripts
│   └── entrypoint.sh
├── src
│   ├── __init__.py
│   ├── agent
│   │   ├── __init__.py
│   │   └── virtual_agent.py
│   ├── client
│   │   ├── __init__.py
│   │   ├── llm_integration.py
│   │   └── main.py
│   ├── database
│   │   ├── __init__.py
│   │   ├── db_session.py
│   │   └── models.py
│   ├── models
│   │   ├── __init__.py
│   │   └── vehicle_model.py
│   └── server
│       ├── __init__.py
│       ├── mcp_server.py
│       └── process_request.py
├── utils
│   ├── __init__.py
│   └── fetch_vehicles_data.py
└── vehicles.db
```
**Checklist do Desafio Técnico – Vaga de Desenvolvedor Python | C2S**


**Tarefas Específicas:**

1.  **Modelagem de Dados:**
    - [x] Criar um esquema de banco de dados para representar automóveis.
    - [x] Incluir pelo menos 10 atributos relevantes (ex: Marca, modelo, ano, motorização, tipo de combustível, cor, quilometragem, número de portas, transmissão, preço, etc.).

2.  **Popular o Banco com Dados Fictícios:**
    - [x] Desenvolver um script para inserir dados fictícios no banco de dados.
    - [x] Inserir no mínimo 100 veículos simulados (fakes).
    - [x] Usar bibliotecas como Faker, SQLAlchemy, Pandas, ou outras de preferência.

3.  **Comunicação Cliente-Servidor via Protocolo MCP:**
    - [x] Implementar a comunicação entre um cliente e um servidor usando um "Protocolo de Contexto de Modelo" (MCP) customizado.
    - [x] O cliente deve enviar filtros (como marca, ano, tipo de combustível) para o servidor.
    - [x] O servidor deve interpretar os filtros.
    - [x] O servidor deve consultar o banco de dados com base nos filtros.
    - [x] O servidor deve retornar os resultados para o cliente.
    - [x] Garantir que não haja consultas diretas ao banco de dados pelo cliente; o fluxo deve ser Cliente -> Servidor -> Banco de Dados.

4.  **Aplicação no Terminal com Agente Virtual:**
    - [x] Criar uma aplicação que roda diretamente no terminal.
    - [x] Implementar um agente virtual interativo.
    - [x] O agente deve iniciar a conversa ao iniciar a aplicação (sem "menuzão" de IF/ELSE).
    - [x] O agente deve entender o que o usuário está procurando.
    - [x] O agente deve fazer perguntas para esclarecer a busca (ex: marca, modelo, ano, combustível, faixa de preço).
    - [x] As perguntas não devem seguir um padrão engessado tipo formulário; permitir interação mais fluida.
    - [x] O agente deve receber os veículos compatíveis do servidor.
    - [x] O agente deve exibir os resultados em uma resposta amigável.
    - [x] Os resultados exibidos devem incluir: marca, modelo, ano, cor, quilometragem e preço (ou outros atributos relevantes definidos na etapa 1).

## Ferramentas necessárias

- Python 3.12
- Docker
## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar das seguintes variáveis de ambiente no seu .env

- `OLLAMA_MODEL`

essa variável contem o nome do modelo llama a ser usado, caso queria encontrar modelos a para utilizar você pode procurar no próprio [site do ollama](https://ollama.com/library) 

Inicialmente ja esta tudo preparado caso não queira modificar nada rode o seguinte comando:

*Para isso foi utilizada para testes apenas o modelo: llama3.1:8b*

- `OLLAMA_HOST`

Essa variável armazena o host do ollama

*Inicialmente ja esta tudo preparado caso não queira modificar nada rode o seguinte comando:*

```bash
   cp .env.sample .env
```
## Execução

Primeiro baixe o o repositório:

```bash
  git clone https://github.com/VitorManoel0/VeiculosLLM.git
```

Entre no diretório do projeto

```bash
  cd VeiculosLLM
```

Iniciar a aplicação:

```bash
  make run-all
```

caso você tenha saido da aplicação e queria voltar rode o seguinte comando:

```bash
  make run-app
```

Ao finalizar tudo para remover os containêrs:

```bash
  docker-compose down -v
```

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


