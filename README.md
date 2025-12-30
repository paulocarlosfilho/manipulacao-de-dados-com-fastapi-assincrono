# Manipulação de Dados com FastAPI Assíncrono

Este projeto demonstra como realizar a manipulação de dados de forma assíncrona utilizando FastAPI, SQLAlchemy e PostgreSQL via Docker.

## 🚀 Tecnologias
- **FastAPI**: Framework web moderno e rápido.
- **PostgreSQL**: Banco de dados relacional.
- **SQLAlchemy (Async)**: ORM para mapeamento objeto-relacional assíncrono.
- **Docker & Docker Compose**: Para orquestração do banco de dados.
- **Makefile**: Para facilitar a execução de comandos comuns.

## 🛠️ Como rodar o projeto

### Pré-requisitos
- Docker e Docker Compose instalados.
- Python 3.8+ instalado.
- WSL 2 (recomendado para Windows).

### Passo a Passo

1. **Subir o Banco de Dados (PostgreSQL)**
   ```bash
   wsl make up
   ```

2. **Instalar Dependências (Cria Ambiente Virtual)**
   ```bash
   wsl make install
   ```
   *Este comando cria automaticamente um ambiente virtual (`.venv`) para evitar conflitos com o sistema.*

3. **Executar a Aplicação**
   ```bash
   wsl make run-app
   ```
   A aplicação estará disponível em `http://localhost:8000`.

4. **Acessar Documentação (Swagger)**
   Acesse `http://localhost:8000/docs` para interagir com a API.

## 📁 Estrutura de Arquivos
- `main.py`: Ponto de entrada da aplicação FastAPI.
- `database.py`: Configuração da conexão assíncrona com o PostgreSQL.
- `post.py`: Definição da tabela/modelo de Posts.
- `docker-compose.yml`: Configuração do container PostgreSQL.
- `Makefile`: Atalhos para comandos frequentes.
- `requirements.txt`: Lista de dependências do Python.

## ⚙️ Configuração do Banco de Dados
O banco de dados é configurado via `database.py` e utiliza a seguinte URL de conexão por padrão:
`postgresql+asyncpg://user:password@localhost/blog_db`

As tabelas são criadas automaticamente ao iniciar a aplicação através do evento `@app.on_event("startup")`.
