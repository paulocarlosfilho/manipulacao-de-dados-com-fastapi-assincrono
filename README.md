# Manipulação de Dados com FastAPI Assíncrono

![Frontend Dashboard](2.png)
*Interface moderna do projeto construída com Tailwind CSS*

---

![Backend Code and Tests](1.png)
*Estrutura de código assíncrono e execução de testes automatizados*

---

Este projeto demonstra como realizar a manipulação de dados de forma assíncrona utilizando FastAPI, SQLAlchemy e PostgreSQL via Docker, incluindo autenticação JWT e testes automatizados.

---

## 💼 Portfólio e Carreira
Para uma visão detalhada das competências técnicas aplicadas neste projeto, consulte o arquivo [PORTFOLIO.md](PORTFOLIO.md). Ele foi estruturado para auxiliar em processos seletivos e demonstrações técnicas.

---

## 🚀 Tecnologias
- **FastAPI**: Framework web moderno e rápido.
- **PostgreSQL**: Banco de dados relacional.
- **SQLAlchemy (Async)**: ORM para mapeamento objeto-relacional assíncrono.
- **Docker & Docker Compose**: Para orquestração do banco de dados.
- **JWT (JSON Web Tokens)**: Autenticação segura com Bearer tokens.
- **Pytest**: Suíte de testes automatizados assíncronos.
- **Makefile**: Para facilitar a execução de comandos comuns no ambiente WSL.

## 🛠️ Como rodar o projeto

### Pré-requisitos
- Docker e Docker Compose instalados.
- Python 3.10+ instalado.
- WSL 2 (obrigatório para uso do Makefile no Windows).

### Passo a Passo

1. **Subir o Banco de Dados (PostgreSQL)**
   ```bash
   wsl make up
   ```

2. **Instalar Dependências (Cria Ambiente Virtual)**
   ```bash
   wsl make install
   ```
   *Este comando cria automaticamente um ambiente virtual (`.venv`) e instala todas as dependências, incluindo correções de compatibilidade para `bcrypt`.*

3. **Executar a Aplicação**
   ```bash
   wsl make run-app
   ```
   A aplicação estará disponível em `http://localhost:8000`. 
   *O frontend será carregado automaticamente na raiz `/`.*

4. **Interface Gráfica (Frontend)**
   O projeto agora conta com uma interface moderna construída com **Tailwind CSS**. 
   - **Login**: Autenticação via JWT.
   - **Dashboard**: Visualização e criação de posts em tempo real.
   - **Exclusão**: Gerenciamento de posts diretamente pela interface.

5. **Executar os Testes**
   ```bash
   wsl make test
   ```
   Executa a suíte completa de testes de autenticação e CRUD de posts.

6. **Acessar Documentação (Swagger)**
   Acesse `http://localhost:8000/docs` para interagir com a API.

7. **Infraestrutura na AWS (Terraform)**
   Para gerenciar a infraestrutura na nuvem:
   - `wsl make tf-init`: Inicializa o Terraform.
   - `wsl make tf-plan`: Visualiza as mudanças que serão feitas.
   - `wsl make tf-apply`: Cria os recursos na AWS.
   - `wsl make tf-destroy`: **Remove** tudo para evitar cobranças indesejadas.

## 📁 Estrutura de Arquivos

- `app/`: Pasta principal da aplicação.
  - `main.py`: Ponto de entrada e configuração do FastAPI com `lifespan`.
  - `auth.py`: Lógica de autenticação JWT, hashing de senhas e segurança.
  - `database.py`: Configuração da conexão assíncrona com PostgreSQL.
  - `models/`: Definições de tabelas e esquemas Pydantic.
  - `routers/`: Rotas da API (Posts, etc).
- `tests/`: Suíte de testes automatizados.
- `docker-compose.yml`: Configuração do container PostgreSQL 15.
- `Makefile`: Atalhos para comandos frequentes no ambiente WSL.
- `pytest.ini`: Configurações do ambiente de testes assíncronos.

## 🔐 Autenticação
A API utiliza autenticação **Bearer Token (JWT)**.
- **Token Expiration**: 30 minutos.
- **Claims**: iss, aud, exp, iat, nbf, jti.
- **Credenciais de Teste**: 
  - Usuário: `admin`
  - Senha: `admin123`

## ⚙️ Configuração do Banco de Dados
O banco utiliza `SQLAlchemy` com `asyncpg`. A criação das tabelas ocorre automaticamente na inicialização da aplicação através do gerenciador de contexto `lifespan`.

---

## 🚀 Roadmap e Próximos Passos (IaC)

O projeto já conta com a base de código para automação de infraestrutura, permitindo que o próximo passo seja o deploy automatizado:

### **Implementação de Infraestrutura como Código (IaC)**
- [x] **Dockerization**: `Dockerfile` pronto para produção.
- [x] **Orquestração**: `docker-compose.yml` para ambientes locais e cloud.
- [x] **Provisionamento AWS**: Arquivos de **Terraform** criados e prontos para uso na pasta `terraform/`.
- [ ] **Deploy em Produção**: Executar o Terraform para subir a instância EC2 real.
- [x] **CI/CD Pipeline**: Configurar GitHub Actions para automação de testes e deploy.
