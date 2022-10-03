.DEFAULT_GOAL = help
.PHONY: help setup test build publish

PYTHON_BIN ?= "/usr/bin/env python3"

help:
	@echo --HELP--
	@echo make help - display this message
	@echo make setup - install dependencies
	@echo make test - run tests
	@echo make build - build package
	@echo make publish - upload package to pypi

	@echo "(python binary: "\"${PYTHON_BIN}\"")"

setup:
	@echo --SETUP--
	${PYTHON_BIN} -m pip install poetry
	${PYTHON_BIN} -m poetry install

test:
	@echo --TEST--
	${PYTHON_BIN} -m poetry run python -m pytest -p no:sugar
	${PYTHON_BIN} -m poetry run mypy simplematrixbotlib --ignore-missing-imports
	${PYTHON_BIN} -m poetry run python -m bandit -r simplematrixbotlib

build:
	@echo --BUILD--
	${PYTHON_BIN} -m poetry build

publish:
	@echo --PUBLISH--
	${PYTHON_BIN} -m poetry publish
