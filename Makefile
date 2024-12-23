VENV_DIR=.venv
PYTHON=$(VENV_DIR)/bin/python

.ONESHELL:

.venv:
	python -m venv $(VENV_DIR)

install: .venv
	$(PYTHON) -m pip install -r requirements.txt

run: install
	$(PYTHON) main.py

clean:
	rm -rf $(VENV_DIR)
