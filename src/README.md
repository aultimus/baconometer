# Baconometer

## Running in the Debugger (VS Code)

We recommend the following VS Code extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) 

1. Open the project folder in VS Code.
2. Go to the Run and Debug panel (play icon in the sidebar).
3. Select "Python: Flask" from the dropdown.
4. Click the green "Run" button or press F5.
5. Set breakpoints in your Python files as needed.

## Using the Makefile

From the top-level project directory, you can use the following commands:

- `make install` – Installs Python dependencies from `src/requirements.txt`.
- `make run` – Runs the Flask app (served from `src/app.py`).
- `make download-datasets` – Downloads the IMDb dataset files (`name.basics.tsv.gz` and `title.basics.tsv.gz`) into the top-level directory.

Example usage:

```bash
make install
make run
make download-datasets
```

## Features to add
- Caching of results
- BFS search
- SQL Database
- Map of an actor
