# Baconometer

## Dev setup

- `make install` – Installs Python dependencies from `requirements.txt` (or via Poetry if configured).

## Downloading and Preparing Data

You should only need to do this once or whenever you want to load new data. The import is the really slow step, this initialises the neo4j database but takes around eight minutes to complete.

- `make download-datasets` – Downloads the IMDb dataset files (`name.basics.tsv.gz` and `title.basics.tsv.gz`) into the top-level directory.
- `make import-to-neo4j` – Imports actors and films from the .tsv files into Neo4j. See `src/import_to_neo4j.py`.
- `make prepare-data` – Fenerates the Neo4j bulk import CSVs (`actors.csv`, `films.csv`, `acted_in.csv`). Run this before importing data into Neo4j for the first time or after updating the datasets via `make download-data`.
- `make import-data` – Runs the Neo4j bulk import step using Docker Compose. This loads the generated CSVs into a fresh Neo4j database.

## Testing

- `make test` – Runs the test suite using pytest with the correct import path setup.

## Running

- `make up-dev` – Starts the full stack (Neo4j and your app) using Docker Compose.

### Running in the Debugger (VS Code)

We recommend the following VS Code extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) 

1. Open the project folder in VS Code.
2. Go to the Run and Debug panel (play icon in the sidebar).
3. Select "Python: Flask" from the dropdown.
4. Click the green "Run" button or press F5.
5. Set breakpoints in your Python files as needed.

Note, you will need to run the database in the background in order to do this. TODO: write steps.

## Features to add
- Caching of results
- BFS search
- Map of an actor
- Wait for db to come up before fully initialising service