# Variáveis
PYTHON = python3
VENV = /home/$(USER)/.venv_blog
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn
DOCKER_COMPOSE = docker compose

.PHONY: help install up down restart run-app clean test ci-local k8s-cluster k8s-deploy k8s-status k8s-delete k8s-load-image k8s-forward k8s-logs k8s-monitoring k8s-grafana k8s-prometheus k8s-grafana-url

help:
	@echo "Comandos disponíveis:"
	@echo "  install    - Cria venv (no HOME do WSL) e instala as dependências"
	@echo "  up         - Sobe o banco de dados PostgreSQL via Docker"
	@echo "  down       - Para o banco de dados PostgreSQL"
	@echo "  restart    - Reinicia o banco de dados"
	@echo "  run-app    - Inicia a aplicação FastAPI usando o venv"
	@echo "  clean      - Remove venv, __pycache__ e o banco SQLite antigo"
	@echo "  test       - Executa os testes automatizados"
	@echo "  test-cov   - Executa os testes com relatório de cobertura"
	@echo "  ci-local   - Simula o pipeline de CI localmente (Docker + Testes)"
	@echo ""
	@echo "Orquestração Kubernetes (Kind):"
	@echo "  k8s-cluster    - Cria o cluster multi-node (1 CP, 3 Workers)"
	@echo "  k8s-deploy     - Aplica os manifestos (Deployment, Service, ConfigMap)"
	@echo "  k8s-status     - Mostra o status dos Pods, Nodes e Services"
	@echo "  k8s-delete     - Deleta o cluster Kubernetes local"
	@echo "  k8s-load-image - Carrega a imagem local do Docker no Kind"
	@echo "  k8s-forward    - Cria um túnel para acessar a API em localhost:8000"
	@echo "  k8s-logs       - Mostra os logs da aplicação no cluster (tempo real)"
	@echo "  k8s-monitoring - Instala Prometheus e Grafana no cluster"
	@echo "  k8s-grafana    - Abre o túnel para o Grafana em localhost:3000"
	@echo "  k8s-prometheus - Abre o túnel para o Prometheus em localhost:9090"
	@echo "  k8s-grafana-url- Mostra as credenciais do Grafana"

install:
	rm -rf $(VENV)
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
	export PYTHONPATH=$$PYTHONPATH:. && export DATABASE_URL="postgresql+asyncpg://user:password@localhost/blog_db" && .venv/bin/pytest tests/ -v

test-cov:
	export PYTHONPATH=$$PYTHONPATH:. && export DATABASE_URL="postgresql+asyncpg://user:password@localhost/blog_db" && .venv/bin/pytest --cov=app tests/ -v

ci-local: down up test
	@echo "Pipeline local finalizado com sucesso! Pronto para o push."

# Kubernetes
k8s-cluster:
	kind create cluster --config kind-config.yaml --name dev-cluster

k8s-deploy:
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/deployment.yaml

k8s-status:
	kubectl get nodes -o wide
	kubectl get pods -o wide
	kubectl get svc

k8s-delete:
	kind delete cluster --name dev-cluster

k8s-load-image:
	docker build -t fastapi-app:latest .
	kind load docker-image fastapi-app:latest --name dev-cluster

k8s-forward:
	kubectl port-forward service/fastapi-service 8000:80

k8s-logs:
	kubectl logs -l app=fastapi -f --tail=100

k8s-monitoring:
	kubectl apply -f k8s/monitoring.yaml

k8s-grafana:
	kubectl port-forward svc/grafana-service 3000:3000 -n monitoring

k8s-prometheus:
	kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring

k8s-grafana-url:
	@echo "Acesse o Grafana em: http://localhost:3000"
	@echo "Usuário: admin"
	@echo "Senha: admin"
