# Makefile for running the Flask app and managing datasets

.PHONY: install run download-data create-venv test import-to-neo4j compose-up download-data prepare-data

create-venv:
	@if [ ! -d .venv ]; then python3 -m venv .venv; echo "Python virtual environment created in .venv"; else echo ".venv already exists"; fi

install: create-venv
	. .venv/bin/activate && pip install -r src/requirements.txt

test:
	. .venv/bin/activate && PYTHONPATH=src pytest src/tests/

import-to-neo4j:
	. .venv/bin/activate && pip install -r src/requirements.txt && python src/import_to_neo4j.py

up-dev:
	docker-compose up --build

download-data:
	curl -O https://datasets.imdbws.com/name.basics.tsv.gz && curl -O https://datasets.imdbws.com/title.basics.tsv.gz

prepare-data:
	. .venv/bin/activate && python src/generate_neo4j_bulk_csvs.py

import-data:
	docker compose -f docker-compose.import.yml run import

