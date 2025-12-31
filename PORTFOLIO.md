# Portfólio Técnico: API de Blog Assíncrona com Cloud & DevOps

Este documento serve como um guia técnico para recrutadores e gestores, detalhando as competências de engenharia aplicadas neste projeto por **Paulo Carlos Filho**.

## 📌 Visão Geral
Este projeto não é apenas um sistema de blog; é uma demonstração de competência em **Backend moderno**, **Segurança**, **Containerização** e **Infraestrutura como Código (IaC)**. Ele reflete a transição acadêmica (IFPE) para a aplicação prática em Cloud Computing.

---

## 🏗️ Pilares Técnicos

### 1. Backend & Performance (Python/FastAPI)
- **Assincronismo (Async/Await)**: Toda a camada de dados utiliza `SQLAlchemy` com drivers assíncronos (`asyncpg`), garantindo que a aplicação não bloqueie durante operações de I/O, suportando maior volume de requisições simultâneas.
- **Lifespan Management**: Implementação do ciclo de vida do FastAPI para gerenciar a inicialização do banco de dados e limpeza de recursos.
- **Pydantic V2**: Uso de modelos de dados rigorosos para validação e serialização automática.

### 2. Segurança & Autenticação (JWT)
- **OAuth2 & Bearer Tokens**: Implementação completa de autenticação usando JSON Web Tokens.
- **Segurança de Senhas**: Utilização de `bcrypt` (através do `passlib`) para hashing seguro de senhas no banco de dados.
- **Token Claims**: Configuração de claims padrão (`exp`, `iss`, `aud`, `iat`) para conformidade com padrões de segurança da indústria.

### 3. Infraestrutura & Cloud (AWS/Terraform)
- **Infraestrutura como Código (IaC)**: Provisionamento de uma infraestrutura completa na **AWS** via **Terraform**, incluindo:
  - **Rede Customizada**: VPC, Subnets Públicas, Internet Gateway e Route Tables.
  - **Compute**: Instância EC2 configurada via `user_data` para instalação automática de dependências.
  - **Segurança**: Security Groups restritivos para tráfego HTTP e SSH.
- **Orquestração**: Utilização de **Docker e Docker Compose** para garantir que o ambiente de desenvolvimento seja idêntico ao de produção.

### 4. Automação & Qualidade (DevOps/CI-CD)
- **CI/CD Pipeline**: Implementação de um pipeline de **Continuous Integration** via **GitHub Actions**. O projeto é validado automaticamente em cada `push`, executando:
  - Provisionamento de um banco de dados PostgreSQL efêmero para testes.
  - Instalação automatizada de dependências.
  - Execução da suíte completa de testes assíncronos.
- **Testes Automatizados**: Suíte de testes com **Pytest** cobrindo fluxos críticos de CRUD e Autenticação.
- **Makefile**: Padronização de comandos para instalação, execução de testes, gerenciamento de containers e operações do Terraform.

---

## 📈 Impacto Profissional
A construção deste projeto demonstra capacidade de:
1. **Resolver problemas complexos**: Como migração de bancos de dados e resolução de dependências em ambientes isolados (WSL/Venv).
2. **Pensar em Escala**: Escolha de ferramentas (PostgreSQL, FastAPI) voltadas para performance.
3. **Gerenciar Infraestrutura**: Visão além do código, focando em como a aplicação é entregue e mantida na nuvem.

---

## 🔗 Contatos e Links
- **LinkedIn**: [paulocarlosfilho](https://www.linkedin.com/in/paulocarlosfilho)
- **GitHub**: [Paulo Filho](https://github.com/paulocarlosfilho)
- **E-mail**: paulocarlosfilho@gmail.com
