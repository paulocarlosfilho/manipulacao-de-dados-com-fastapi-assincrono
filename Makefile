# Variáveis
PYTHON = python3
VENV = .venv
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn
DOCKER_COMPOSE = docker compose

.PHONY: help install up down restart run-app clean test tf-init tf-plan tf-apply tf-destroy ci-local

help:
	@echo "Comandos disponíveis:"
	@echo "  install    - Cria venv e instala as dependências"
	@echo "  up         - Sobe o banco de dados PostgreSQL via Docker"
	@echo "  down       - Para o banco de dados PostgreSQL"
	@echo "  restart    - Reinicia o banco de dados"
	@echo "  run-app    - Inicia a aplicação FastAPI usando o venv"
	@echo "  clean      - Remove venv, __pycache__ e o banco SQLite antigo"
	@echo "  test       - Executa os testes automatizados"
	@echo "  tf-init    - Inicializa o Terraform"
	@echo "  tf-plan    - Mostra o plano de execução do Terraform"
	@echo "  tf-apply   - Aplica as mudanças do Terraform na AWS"
	@echo "  tf-destroy - Destrói toda a infraestrutura na AWS (Cuidado!)"
	@echo "  ci-local   - Simula o pipeline de CI localmente (Docker + Testes)"

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart

run-app:
	$(UVICORN) app.main:app --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf $(VENV)
	rm -f blog.db

test:
	export PYTHONPATH=$$PYTHONPATH:. && export DATABASE_URL="postgresql+asyncpg://user:password@localhost/blog_db" && $(VENV)/bin/pytest tests/ -v

tf-init:
	terraform -chdir=terraform init

tf-plan:
	terraform -chdir=terraform plan

tf-apply:
	terraform -chdir=terraform apply -auto-approve

tf-destroy:
	terraform -chdir=terraform destroy -auto-approve

ci-local: down up test
	@echo "Pipeline local finalizado com sucesso! Pronto para o push."
