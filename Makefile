PIP = pip3
PYTHON = python3

.PHONY = help ci-lint coverage lint pre-lint setup test
.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To check the project coverage type make coverage"
	@echo "To lint the project type make lint"
	@echo "To setup the project type make setup"
	@echo "To test the project type make test"
	@echo "------------------------------------"

coverage:
	${PIP} install coverage
	coverage run setup.py test

ci-lint: pre-lint lint

pre-lint:
	${PIP} install pylint
	${PIP} install setuptools-lint
	${PIP} install --upgrade pep8
	${PIP} install --upgrade autopep8

lint:
	${PYTHON} setup.py lint
	autopep8 --in-place -r castle

setup:
	${PYTHON} setup.py install

test:
	${PYTHON} setup.py test
