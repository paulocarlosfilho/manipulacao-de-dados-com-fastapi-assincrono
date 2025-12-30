# Variáveis
PYTHON = python3
VENV = .venv
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn
DOCKER_COMPOSE = docker compose

.PHONY: help install up down restart run-app clean

help:
	@echo "Comandos disponíveis:"
	@echo "  install   - Cria venv e instala as dependências"
	@echo "  up        - Sobe o banco de dados PostgreSQL via Docker"
	@echo "  down      - Para o banco de dados PostgreSQL"
	@echo "  restart   - Reinicia o banco de dados"
	@echo "  run-app   - Inicia a aplicação FastAPI usando o venv"
	@echo "  clean     - Remove venv, __pycache__ e o banco SQLite antigo"

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
	$(UVICORN) main:app --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf $(VENV)
	rm -f blog.db
