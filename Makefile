include .env
export

OLLAMA_MODEL ?= llama3.1:8b

lint:
	ruff format .
	ruff check . --fix

run-docker:
	docker compose up -d
	docker exec -it veiculosllm-ollama-1 ollama pull $(OLLAMA_MODEL)

build-app:
	docker compose build app

run-app:
	docker compose run --rm --service-ports app

enter-container:
	docker compose run --rm --service-ports app /bin/bash

run-all:
	make run-docker && make build-app && make run-app


cleanup:
	docker compose down -v
