init:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

precommit-install:
	pre-commit install

precommit-run:
	pre-commit run --all-files
