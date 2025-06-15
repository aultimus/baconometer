from flask import Flask, render_template, jsonify
from neo4j import GraphDatabase
import os

app = Flask(__name__)

# Neo4j connection setup
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "test")),
)


@app.route("/")
def verify_import():
    with driver.session() as session:
        actor_count = session.run("MATCH (a:Actor) RETURN count(a) AS count").single()[
            "count"
        ]
        film_count = session.run("MATCH (f:Film) RETURN count(f) AS count").single()[
            "count"
        ]
        rel_count = session.run(
            "MATCH (:Actor)-[r:ACTED_IN]->(:Film) RETURN count(r) AS count"
        ).single()["count"]
    return jsonify(
        {
            "actors": actor_count,
            "films": film_count,
            "acted_in_relationships": rel_count,
        }
    )
