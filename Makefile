# Makefile for running the Flask app and managing datasets

.PHONY: install run download-imdb-data create-venv test import-to-neo4j compose-up download-imdb-data prepare-data create-indexes unit-tests integration-tests system-tests test up-dev

install:
	poetry install
	pip install -e .

unit-tests:
	poetry run pytest tests/unit-tests/

integration-tests:
	poetry run pytest tests/integration-tests/

system-tests:
	poetry run pytest tests/system-tests/

test:
	$(MAKE) unit-tests
	$(MAKE) integration-tests
	$(MAKE) system-tests

run:
	docker-compose up

download-imdb-data:
	curl -O https://datasets.imdbws.com/name.basics.tsv.gz && gunzip name.basics.tsv.gz && curl -O https://datasets.imdbws.com/title.basics.tsv.gz && gunzip title.basics.tsv.gz

prepare-data:
	poetry run python scripts/generate_neo4j_bulk_csvs.py

import-data:
	docker compose -f docker-compose.import.yml run import

run-neo4j:
	docker compose -f docker-compose.yml up neo4j

create-indexes:
	docker exec -i neo4j \
		cypher-shell -u neo4j -p neo4jtest123 -f /import/indexes.cypher
