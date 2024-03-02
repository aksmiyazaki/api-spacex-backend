.PHONY: help
help:
	$(info setup - sets the project dependencies. If you are running this locally, please set a virtual environment for it.)
	$(info setup-dev - sets the project dependencies for DEVELOPMENT. If you are running this locally, please set a virtual environment for it.)
	$(info test - runs pytest on the project)
	$(info test-coverage - runs pytest + coverage analysis, oppening a chrome with the report.)

.PHONY: setup
setup:
	pip install -r requirements.txt

.PHONY: setup-dev
setup-dev: setup
	pip install -r requirements-dev.txt

.PHONY: test
test:
	python -m pytest

.PHONY: test-coverage
test-coverage:
	coverage run -m pytest src/tests -source=.
	coverage report --omit="*__init__.py,tests/*,*/site-packages/*" -m
	coverage html --omit="*__init__.py,tests/*,*/site-packages/*" && open htmlcov/index.html
