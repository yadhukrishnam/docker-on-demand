PROJECT_DIR=dockinator
VENV_DIR=venv
REQ_FILE=$(PROJECT_DIR)/requirements.txt
MANAGE=$(PROJECT_DIR)/manage.py
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip
CRON_SCRIPT=etc/cron.sh

.PHONY: venv
venv:
	python3 -m venv $(VENV_DIR)

.PHONY: install
install: venv
	$(PIP) install -r $(REQ_FILE)

.PHONY: migrate
migrate:
	$(PYTHON) $(MANAGE) migrate

.PHONY: runserver
runserver:
	$(PYTHON) $(MANAGE) runserver

.PHONY: createsuperuser
createsuperuser:
	$(PYTHON) $(MANAGE) createsuperuser

.PHONY: shell
shell:
	$(PYTHON) $(MANAGE) shell

.PHONY: collectstatic
collectstatic:
	$(PYTHON) $(MANAGE) collectstatic --noinput

.PHONY: clean
clean:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "__pycache__" -exec rm -rf {} \;

.PHONY: cmd
cmd:
	$(PYTHON) $(MANAGE) $(COMMAND)

.PHONY: black
black:
	$(VENV_DIR)/bin/black $(PROJECT_DIR)

.PHONY: ruff
ruff:
	$(VENV_DIR)/bin/ruff $(PROJECT_DIR)

.PHONY: lint
lint: 
	ruff check 

.PHONY: cron
cron:
	$(PYTHON) $(MANAGE) manage_expired --kill-expired