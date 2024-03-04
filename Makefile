application_container_name=spacex-parser-application
database_container_name=postgres-database

.PHONY: help
help:
	$(info setup - sets the project dependencies. If you are running this locally, please set a virtual environment for it.)
	$(info setup-dev - sets the project dependencies for DEVELOPMENT. If you are running this locally, please set a virtual environment for it.)
	$(info test - runs pytest on the project)
	$(info test-coverage - runs pytest + coverage analysis, oppening a chrome with the report.)
	$(info build-image - builds application's docker image.)
	$(info docker-clean - cleans docker environment, usually used after a dockerized run.)
	$(info dockerized-run-small-workload - runs the application with a small workload.)
	$(info dockerized-run-huge-workload - runs the application with a huge workload.)
	$(info query-local - queries the database with local psql.)
	$(info query-on-container - queries the database with dockerized psql.)

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
	coverage report --omit="*__init__.py,src/tests/*,*/site-packages/*" -m
	coverage html --omit="*__init__.py,src/tests/*,*/site-packages/*" && open htmlcov/index.html

.PHONY: build-image
build-image:
	docker build -t spacex-parser -f ./docker/application/Dockerfile .
	docker build -t initialized-database -f ./docker/database/Dockerfile .

.PHONY: docker-clean
docker-clean:
	docker stop $(application_container_name) $(database_container_name)
	docker container rm $(application_container_name) $(database_container_name)

.PHONY: dockerized-run-small-workload
dockerized-run-small-workload:
	docker build -t spacex-parser -f ./docker/application/Dockerfile .
	CONFIG_FILE=./resources/configs/config-small.json docker-compose -f docker/spin-docker-and-application.yml up

.PHONY: dockerized-run-huge-workload
dockerized-run-huge-workload:
	docker build -t spacex-parser -f ./docker/application/Dockerfile .
	CONFIG_FILE=./resources/configs/config-huge.json docker-compose -f docker/spin-docker-and-application.yml up

.PHONY: query-local
query-local:
	PGPASSWORD=mysecretpassword psql -h localhost -U postgres -d spacex -c "SELECT * FROM satellite WHERE satellite_id='$(id_to_fetch)' AND creation_date < '$(creation_date)' ORDER BY creation_date DESC LIMIT 1;"


.PHONY: query-on-container
query-on-container:
	PGPASSWORD=mysecretpassword psql -h localhost -U postgres -d spacex -c "SELECT * FROM satellite WHERE satellite_id='$(id_to_fetch)' AND creation_date < '$(creation_date)' ORDER BY creation_date DESC LIMIT 1;"