FROM python:3.10-slim

WORKDIR /app

COPY src/requirements.txt ./src/requirements.txt
RUN pip install --no-cache-dir -r src/requirements.txt

COPY src/ ./src/
COPY name.basics.tsv ./
COPY title.basics.tsv ./

# Default command (can be overridden by docker-compose)
CMD ["python", "src/import_to_neo4j.py"]
