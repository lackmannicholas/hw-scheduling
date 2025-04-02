# Makefile for Python project

venv:
	python3 -m venv .venv
	@echo "Virtual environment created. Activate it using 'source .venv/bin/activate'"
	@echo "Then run 'make install' to install dependencies."
	@echo "To deactivate, run 'deactivate'"
	@echo "To remove the virtual environment, run 'make clean'"
clean:
	rm -rf .venv
	@echo "Virtual environment removed."

install:
	@echo "Installing dependencies..."
	@echo "Make sure to activate the virtual environment first using 'make venv'"
	pip install -r requirements.txt

run:
	python3 main.py

test:
	pytest -v --disable-warnings