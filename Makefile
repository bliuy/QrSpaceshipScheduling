# Defining makefile variables
VENV = venv
PYTHON = $(VENV)/bin/python3 # Path to python3 runner in the virtualenv
PIP = $(VENV)/bin/pip # Path to pip utility in the virtualenv

run: installing-dependencies
	@echo "Starting Makefile build."
	@pwd
	$(PYTHON) -m src/main

installing-dependencies: creating-virtualenv
	$(PIP) install fastapi
	$(PIP) install "uvicorn[standard]"
	$(PIP) install pydantic

creating-virtualenv: install-virtualenv
	python3 -m venv $(VENV)

install-virtualenv:
	@echo "Installing python3.10-venv." 
	sudo apt install python3.10-venv

clean:
	rm -rf $(VENV) # Removing virtualenv
