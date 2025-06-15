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
def home():
    return "baconometer"
    # return render_template("index.html")


@app.route("/verify_import", methods=["GET"])
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


@app.route("/bacon-number/<actorA>/<actorB>", methods=["GET"])
def bacon_number(actorA, actorB):
    """
    Returns the Bacon number (shortest path length) and the list of films connecting two actors by their names.
    Example: /bacon-number/Kevin%20Bacon/Tom%20Hanks
    """
    with driver.session() as session:
        result = session.run(
            """
            MATCH (a:Actor {name: $actorA}), (b:Actor {name: $actorB})
            MATCH p=shortestPath((a)-[:ACTED_IN*]-(b))
            WITH p, [n IN nodes(p) WHERE n:Film | n.title] AS films
            RETURN length(p)/2 AS bacon_number, films
            """,
            {"actorA": actorA, "actorB": actorB},
        )
        record = result.single()
        if record and record["bacon_number"] is not None:
            return jsonify(
                {
                    "bacon_number": int(record["bacon_number"]),
                    "films": record["films"],
                }
            )
        else:
            return (
                jsonify({"error": "No path found between the given actors by name."}),
                404,
            )
