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