# Makefile for running the Flask app and managing datasets

.PHONY: install run download-datasets create-venv

create-venv:
	@if [ ! -d .venv ]; then python3 -m venv .venv; echo "Python virtual environment created in .venv"; else echo ".venv already exists"; fi

install: create-venv
	. .venv/bin/activate && pip install -r src/requirements.txt

run:
	cd src && export FLASK_APP=app.py && flask run

download-datasets:
	curl -O https://datasets.imdbws.com/name.basics.tsv.gz && curl -O https://datasets.imdbws.com/title.basics.tsv.gz
