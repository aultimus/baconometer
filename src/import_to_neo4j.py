import os
import csv
from neo4j import GraphDatabase
from itertools import islice

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test")

NAME_BASICS_PATH = "name.basics.tsv"
TITLE_BASICS_PATH = "title.basics.tsv"

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def clear_database(tx):
    tx.run("MATCH (n) DETACH DELETE n")


def create_film_nodes(tx, films):
    for film in films:
        tx.run(
            "MERGE (f:Film {titleId: $titleId, title: $title})",
            titleId=film["tconst"],
            title=film["primaryTitle"],
        )


def create_actor_and_relationships(tx, actor, film_ids):
    tx.run(
        "MERGE (a:Actor {nconst: $nconst, name: $name})",
        nconst=actor["nconst"],
        name=actor["primaryName"],
    )
    for title_id in film_ids:
        tx.run(
            "MATCH (a:Actor {nconst: $nconst}), (f:Film {titleId: $titleId}) "
            "MERGE (a)-[:ACTED_IN]->(f)",
            nconst=actor["nconst"],
            titleId=title_id,
        )


def create_film_nodes_batch(tx, films):
    tx.run(
        """
        UNWIND $films AS film
        MERGE (f:Film {titleId: film.tconst, title: film.primaryTitle})
        """,
        films=films,
    )


def create_actors_and_relationships_batch(tx, batch):
    tx.run(
        """
        UNWIND $batch AS row
        MERGE (a:Actor {nconst: row.nconst, name: row.primaryName})
        WITH a, row
        UNWIND row.known_titles AS titleId
        MATCH (f:Film {titleId: titleId})
        MERGE (a)-[:ACTED_IN]->(f)
        """,
        batch=batch,
    )


def load_films_stream():
    with open(TITLE_BASICS_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            yield row


def load_actors_stream():
    with open(NAME_BASICS_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            yield row


def count_lines(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f) - 1  # subtract header


def main():
    print("Counting total films and actors...")
    total_films = count_lines(TITLE_BASICS_PATH)
    total_actors = count_lines(NAME_BASICS_PATH)
    print(f"Total films: {total_films}, total actors: {total_actors}")
    print("Loading film IDs for reference...")
    film_ids_set = set()
    for film in load_films_stream():
        film_ids_set.add(film["tconst"])
    print(f"Found {len(film_ids_set)} films.")
    with driver.session() as session:
        print("Clearing database...")
        session.write_transaction(clear_database)
        print("Creating film nodes in batch...")
        # Stream films in batches
        batch_size = 10000
        film_stream = load_films_stream()
        film_done = 0
        while True:
            batch = list(islice(film_stream, batch_size))
            if not batch:
                break
            session.write_transaction(create_film_nodes_batch, batch)
            film_done += len(batch)
            print(
                f"Created {film_done}/{total_films} films ({film_done*100//total_films}%)"
            )
        print("Creating actor nodes and relationships in batches...")
        actor_stream = load_actors_stream()
        i = 0
        while True:
            batch = []
            for actor in islice(actor_stream, batch_size):
                known_titles = (
                    actor["knownForTitles"].split(",")
                    if actor["knownForTitles"]
                    else []
                )
                known_titles = [tid for tid in known_titles if tid in film_ids_set]
                batch.append(
                    {
                        "nconst": actor["nconst"],
                        "primaryName": actor["primaryName"],
                        "known_titles": known_titles,
                    }
                )
            if not batch:
                break
            session.write_transaction(create_actors_and_relationships_batch, batch)
            i += len(batch)
            print(f"Processed {i}/{total_actors} actors ({i*100//total_actors}%)")
        print(f"Done. Imported {i} actors.")
    print("Done.")


if __name__ == "__main__":
    main()
