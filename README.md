# Baconometer

## Dev setup

- `make install` – Installs Python dependencies from `requirements.txt` (or via Poetry if configured) and creates `.venv` venv.
- ` .venv/bin/activate` – Activate venv. It is recommended to install [pyenv](https://github.com/pyenv/pyenv) to obviate the need for this step.

## Downloading and Preparing Data

You should only need to do this once or whenever you want to load new data. The import is the really slow step, this initialises the neo4j database but takes around eight minutes to complete.

- `make download-datasets` – Downloads the IMDb dataset files (`name.basics.tsv.gz` and `title.basics.tsv.gz`) into the top-level directory.
- `make prepare-data` – Generates the Neo4j bulk import CSVs (`actors.csv`, `films.csv`, `acted_in.csv`).
- `make import-data` – Runs the Neo4j bulk import step using Docker Compose. This loads the generated CSVs into a fresh Neo4j database. To run the bulk import manually (outside Docker), use `scripts/import_neo4j_bulk.sh`.

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

## Example usage

You can either use the Web front end or the JSON API.


### Web Frontend
![Baconometer Frontend](images/baconify-ui.png)


### JSON API
```
(.venv) aulty@aulty-thinkpad:~/src/baconometer$ curl -s localhost:5000/bacon-number/Kevin%20Bacon/Tom%20Hanks | json_pp
{
   "bacon_number" : 2,
   "path" : [
      {
         "actor1" : "Kevin Bacon",
         "actor2" : "E. Scott Mayhugh",
         "film" : "Hollow Man"
      },
      {
         "actor1" : "E. Scott Mayhugh",
         "actor2" : "Tom Hanks",
         "film" : "Forrest Gump"
      }
   ]
}
```

## Debugging Neo4j

To debug the neo4j database, you can use the Neo4j Browser or cypher-shell:

**Using Neo4j Browser:**
1. Open [http://localhost:7474/](http://localhost:7474/) in your web browser.
2. Log in with your Neo4j username and password (default: `neo4j` / `neo4jtest123`).
3. Run commands, e.g.:
   ```
   CALL db.indexes();
   ```

**Using cypher-shell from your host:**
```bash
cypher-shell -u neo4j -p neo4jtest123 -a bolt://localhost:7687 "CALL db.indexes();"
```

**Using cypher-shell inside the container:**
```bash
docker compose exec neo4j cypher-shell -u neo4j -p neo4jtest123 "CALL db.indexes();"
```


## Features to add
- Caching of results
- BFS search
- Map of an actor
- Wait for db to come up before fully initialising service
- Move off of Dev server
- Host
