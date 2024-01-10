VENV_PATH=.venv
VENV_BIN=$(VENV_PATH)/bin

PYTHON_INTERPRETER=python3
PYTHON_BIN=$(VENV_BIN)/python

PIP=$(VENV_BIN)/pip
DJANGO_MANAGE=$(VENV_BIN)/python manage.py
FLAKE=$(VENV_BIN)/flake8
BLACK=$(VENV_BIN)/black

DJANGOPROJECT_DIR=main
DJANGO_SETTINGS=main.settings.local
STATICFILES_DIR=$(DJANGOPROJECT_DIR)/webapp_statics
FRONTEND_DIR=frontend
NPM=npm

# Formatting variables, FORMATRESET is always to be used last to close formatting
FORMATBLUE:=$(shell tput setab 4)
FORMATBOLD:=$(shell tput bold)
FORMATRESET:=$(shell tput sgr0)

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install-backend               -- to install backend requirements with Virtualenv and Pip"
	@echo "  install-frontend              -- to install frontend requirements with Npm"
	@echo "  install-pycheck               -- to install globally Pycheck (WARNING: Have to install/clean manually)"
	@echo "  install                       -- to install backend and frontend"
	@echo
	@echo "  clean                         -- to clean EVERYTHING (WARNING: you cannot recovery from this)"
	@echo "  clean-backend-install         -- to clean backend installation"
	@echo "  clean-db                      -- to clean db files"
	@echo "  clean-frontend-install        -- to clean frontend installation"
	@echo "  clean-frontend-build          -- to clean frontend built files"
	@echo "  clean-pycache                 -- to remove all __pycache__, this is recursive from current directory"
	@echo "  clean-pycheck                 -- to remove Pycheck installation"
	@echo
	@echo "  run                           -- to run Django development server"
	@echo "  check-migrations              -- to check for pending application migrations (do not write anything)"
	@echo "  migrate                       -- to apply database migrations"
	@echo "  migrations                    -- to create database migrations"
	@echo "  superuser                     -- to create a superuser for Django admin"
	@echo "  shell                         -- to open a Django shell"
	@echo
	@echo "  test                          -- run the unit tests"
	@echo
	@echo "  build-front                   -- to build the frontend for production"
	@echo "  front                         -- to run the frontend in dev mode with watch autoreload"
	@echo "  netfront                      -- to run the frontend in dev network mode with watch autoreload"
	@echo "  ws                            -- to run the websockets server"
	@echo "  installws                     -- to install the websockets server"
	@echo "  lm                            -- to run the LM tasks queue"
	@echo
	@echo "  check                         -- to run the check management command"
	@echo "  flake                         -- to launch Flake8 checking"
	@echo "  format                        -- to launch Black formating"
	@echo "  dryformat                     -- to launch Black formating in dry mode"
	@echo "  pycheck                       -- to launch Pycheck code checks"
	@echo "  quality                       -- to launch all quality checks"
	@echo

clean-pycache:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Clear Python cache <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-backend-install:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning backend install <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(VENV_PATH)
.PHONY: clean-backend-install

clean-db:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning db files <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf db.sqlite3
.PHONY: clean-db

clean-frontend-build:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning frontend built files <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(STATICFILES_DIR)/frontend/assets/*
.PHONY: clean-frontend-build

clean-frontend-install:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning frontend install <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(FRONTEND_DIR)/node_modules
	rm -Rf $(FRONTEND_DIR)/yarn.lock
.PHONY: clean-frontend-install

clean: clean-backend-install clean-db clean-frontend-install clean-frontend-build clean-pycache
.PHONY: clean

clean-pycheck:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning Pycheck installation <---$(FORMATRESET)\n"
	@echo ""
	$(NPM) global remove @pycheck/cli
	$(NPM) global remove @pycheck/ui
	rm -Rf yarn.lock
	rm -Rf package.json
	rm -Rf node_modules

install-pycheck:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Installing Pycheck <---$(FORMATRESET)\n"
	@echo ""
	$(NPM) global add @pycheck/cli
	$(NPM) global add @pycheck/ui

venv:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Install virtual environment <---$(FORMATRESET)\n"
	@echo ""
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
	# This is required for those ones using old distribution
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools
.PHONY: venv

install-backend:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Installing backend requirements <---$(FORMATRESET)\n"
	@echo ""
	$(PIP) install -r requirements/dev.txt
.PHONY: install-backend

install-frontend:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Installing frontend requirements <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && $(NPM) install
.PHONY: install-frontend

install: venv install-backend migrate install-frontend
.PHONY: install

shell:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Open a Django shell <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) shell
.PHONY: shell

check-migrations:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Checking for pending project applications models migrations <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) makemigrations --check --dry-run -v 3
.PHONY: check-migrations

migrations:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Apply pending migrations <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) makemigrations
.PHONY: migrations

migrate:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Apply pending migrations <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) migrate
.PHONY: migrate

superuser:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Create a new superuser <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) createsuperuser
.PHONY: superuser

run:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running the backend development server <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) runserver 8000 --settings=${DJANGO_SETTINGS}
.PHONY: run

build-front:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building the frontend <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && $(NPM) build
.PHONY: build-front

front:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running the frontend in dev mode <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && $(NPM) dev
.PHONY: front

ws:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running the websockets server <---$(FORMATRESET)\n"
	@echo ""
	cd centrifugo && ./centrifugo
.PHONY: ws

installws:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Install the websockets server <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) installws --settings=${DJANGO_SETTINGS}
	$(DJANGO_MANAGE) initws --settings=${DJANGO_SETTINGS}
.PHONY: installws

lm:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running the LM tasks queue <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) run_huey --settings=${DJANGO_SETTINGS}
.PHONY: lm

netfront:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running the frontend in dev network mode <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && $(NPM) net
.PHONY: front

test:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Run the tests <---$(FORMATRESET)\n"
	@echo ""
	$(PYTHON_BIN) -m pytest --capture=no
.PHONY: test

check:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Run the manage check command <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) check
.PHONY: check

format:
	$(BLACK) --extend-exclude='/*/migrations/*|setup.py' .
.PHONY: format

dryformat:
	$(BLACK) --extend-exclude='/*/migrations/*|setup.py' --check .
.PHONY: dryformat

pycheck:
	pycheck --django
.PHONY: pycheck

flake:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Flake <---$(FORMATRESET)\n"
	@echo ""
	$(FLAKE) --statistics --show-source $(DJANGOPROJECT_DIR) apps/
.PHONY: flake

quality: check-migrations pycheck
	@echo ""
	@echo "Running quality checks"
	@echo ""
.PHONY: quality
