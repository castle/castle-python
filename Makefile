PIP = pip3
PYTHON = python3

.PHONY = help ci-lint coverage lint format setup test
.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To install the project type make setup"
	@echo "To run the tests type make test"
	@echo "To lint the project type make lint"
	@echo "To auto-format the project type make format"
	@echo "To check coverage type make coverage"
	@echo "------------------------------------"

setup:
	${PIP} install -e ".[test,lint]"

test:
	${PYTHON} -m unittest -v castle.test

lint:
	ruff check castle
	ruff format --check castle

ci-lint: lint

format:
	ruff check --fix castle
	ruff format castle

coverage:
	${PIP} install coverage
	coverage run -m unittest castle.test
	coverage report
