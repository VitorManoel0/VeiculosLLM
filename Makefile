lint:
	ruff format .
	ruff check . --fix

run-setup:
	.venv\Scripts\python.exe -m pip install --upgrade pip
	pip install -r requirements.txt

start-agent-linux:
	python -m venv .venv
	. .venv/bin/activate && make run-setup && python main.py

start-agent-windows:
	python -m venv .venv
	.venv\Scripts\activate && make run-setup && python main.py

run-docker:
	docker compose up -d
	docker exec -it veiculosllm-ollama-1 ollama pull llama3.1:8b

build-app:
	docker compose build app

run-app:
	docker compose run --rm --service-ports app

enter-container:
	docker compose run --rm --service-ports app /bin/bash

run-all:
	make run-docker && make run-app

cleanup:
	docker compose down -v
