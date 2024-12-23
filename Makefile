VENV_DIR=.venv
PYTHON=$(VENV_DIR)/bin/python

.ONESHELL:

.venv:
	python -m venv $(VENV_DIR)
	cp pip.conf $(VENV_DIR)/pip.conf

install: .venv
	export PIP_INDEX_URL=https://pypi.org/simple/
	$(PYTHON) -m pip install -r requirements.txt

run: install
	$(PYTHON) main.py

clean:
	rm -rf $(VENV_DIR)
