# Makefile for running the Flask app and managing datasets

.PHONY: install run download-data create-venv test import-to-neo4j compose-up download-data prepare-data

install:
	pip install -r src/dev-requirements.txt
	pip install -r src/requirements.txt

test:
	PYTHONPATH=src pytest src/tests/

up-dev:
	docker-compose up --build

download-data:
	curl -O https://datasets.imdbws.com/name.basics.tsv.gz && gunzip name.basics.tsv.gz && curl -O https://datasets.imdbws.com/title.basics.tsv.gz && gunzip title.basics.tsv.gz

prepare-data:
	python scripts/generate_neo4j_bulk_csvs.py

import-data:
	docker compose -f docker-compose.import.yml run import

run-neo4j:
	docker compose -f docker-compose.yml run neo4j
