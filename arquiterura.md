# 🏗️ Framework de Desenvolvimento e Engenharia DevOps (Diretrizes Sênior)

Este documento define os padrões arquiteturais, técnicos e de automação que devem ser seguidos. O foco é garantir que o sistema seja "Production-Ready" desde o Localhost, utilizando práticas de SRE (Site Reliability Engineering).

---

## 🛠️ Stack Tecnológica de Referência

### 🔹 Backend & API
- **Framework:** FastAPI (Python 3.10+).
- **Runtime:** Estritamente assíncrono (`async/await`).
- **Data Layer:** SQLAlchemy 2.0 (Async) com Pydantic v2 para validação.
- **Segurança:** Auth JWT + Criptografia BCrypt.

### 🔹 Frontend
- **Framework:** React (Vite) + TypeScript.
- **Estilização:** Tailwind CSS.

### 🔹 Persistência
- **DB:** MySQL 8.0 / PostgreSQL.
- **Segurança de Dados:** Persistência via Volumes e credenciais via Docker Secrets.

---

## 🚀 Automação e CI/CD (Local & Cloud)

Todo código deve ser validado localmente antes do push para o repositório remoto:

### 🛠️ GitHub Actions & nektos/act
- **Local CI:** Uso obrigatório do **`nektos/act`** para rodar workflows do GitHub Actions no Localhost, garantindo ciclos de feedback ultra-rápidos sem custo.
- **CI Pipelines:** Build automático, testes unitários (Pytest/Vitest) e Linting.
- **DevSecOps:** Varredura de vulnerabilidades (Trivy/Snyk) integrada no workflow.
- **CD Strategy:** Deploy via **Rolling Update** no Docker Swarm.

---

## 🔒 Infraestrutura e Resiliência (SRE)

### 🐳 Orquestração (Docker Swarm Mode)
- **Cluster Local:** Desenvolvimento focado em Swarm Mode (`docker swarm init`) para simular o comportamento de produção em ambiente de desenvolvimento.
- **Self-Healing:** Configuração obrigatória de `healthchecks` e `restart_policy` em todos os serviços.
- **Gestão:** Administração visual via Portainer.io local.

### 📊 Observabilidade (Prometheus & Grafana)
- **Metrics:** Exposição do endpoint `/metrics` nativo no Backend.
- **Dashboards:** Monitoramento local de saúde dos containers, latência de requisições e consumo de hardware.

### 🌐 Networking & Security
- **Isolamento:** Uso de redes `overlay` para segregação de tráfego.
- **Secrets:** Gestão de chaves sensíveis via Docker Secrets (Local) e GitHub Secrets (Remote).
- **Hardening:** Containers operando como `non-root` com privilégios mínimos.

---

## 🛠️ Ferramentas de Produtividade (Localhost)
- **Act (CLI):** Para emular o ambiente do GitHub Runners localmente.
- **Makefile:** Abstração de comandos complexos (`make up`, `make test`, `make deploy`).
- **Docker Desktop / Engine:** Engine principal para orquestração de containers.

---
*Manual de Padrões de Engenharia - Foco em DevOps Senior (2026)*