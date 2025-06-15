#!/bin/bash
set -e

# Set paths
DATA_DIR="./neo4j_data_empty"
ACTORS_CSV="actors.csv"
FILMS_CSV="films.csv"
ACTED_IN_CSV="acted_in.csv"
NEO4J_DB_NAME="neo4j"

# Ensure the data directory and databases subdirectory exist and are empty
mkdir -p "$DATA_DIR/databases"
rm -rf "$DATA_DIR/databases/$NEO4J_DB_NAME"

# Run the Neo4j bulk import (requires neo4j-admin in your PATH)
neo4j-admin database import full \
  --nodes=Actor="$ACTORS_CSV" \
  --nodes=Film="$FILMS_CSV" \
  --relationships=ACTED_IN="$ACTED_IN_CSV" \
  --database="$NEO4J_DB_NAME" \
  --force \
  --data-dir="$DATA_DIR"

echo "Bulk import complete. You can now mount $DATA_DIR as your Neo4j data directory."
