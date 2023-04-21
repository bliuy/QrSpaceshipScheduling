# Defining makefile variables
VENV = venv
PYTHON = $(VENV)/bin/python3 # Path to python3 runner in the virtualenv
PIP = $(VENV)/bin/pip # Path to pip utility in the virtualenv
ACTIVATE = $(VENV)/bin/activate

.PHONY: updating-apt

run: updating-apt installing-dependencies run-unittests
	@echo "Starting service."
	$(PYTHON) -m uvicorn --port 8080 src.main:app

installing-dependencies: creating-virtualenv
	$(PIP) install httpx
	$(PIP) install fastapi
	$(PIP) install "uvicorn[standard]"
	$(PIP) install pydantic

creating-virtualenv: install-virtualenv
	python3 -m venv $(VENV)

install-virtualenv:
	@echo "Installing python3.10-venv." 
	sudo apt install python3.10-venv

updating-apt:
	sudo apt-get -y update
	sudo apt-get -y upgrade

run-unittests:
	$(PYTHON) unittests.py

clean:
	rm -rf $(VENV) # Removing virtualenv
