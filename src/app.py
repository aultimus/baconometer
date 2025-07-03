from flask import Flask, render_template, jsonify
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import os
import logging

app = Flask(__name__)

# Neo4j connection setup
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "test")),
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/")
def baconify():
    return render_template("baconify.html")


@app.route("/verify_import", methods=["GET"])
def verify_import():
    try:
        with driver.session() as session:
            actor_count = session.run(
                "MATCH (a:Actor) RETURN count(a) AS count"
            ).single()["count"]
            film_count = session.run(
                "MATCH (f:Film) RETURN count(f) AS count"
            ).single()["count"]
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
    except ServiceUnavailable as e:
        logger.error("Database connection failed: %s", e)
        return jsonify({"error": "Database connection failed"}), 503
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        return jsonify({"error": "Unexpected server error"}), 500


@app.route("/bacon-number/<actorA>/<actorB>")
def bacon_number(actorA, actorB):
    # Convert input names to lowercase for case-insensitive search
    actor_a_lc = actorA.lower()
    actor_b_lc = actorB.lower()
    try:
        with driver.session() as session:
            result = session.run(
                """
                MATCH p = shortestPath(
                    (a:Actor {lowercase_name: $actorA})-
                    [:ACTED_IN*..7]-
                    (b:Actor {lowercase_name: $actorB})
                )
                WITH relationships(p) AS rels, nodes(p) AS ns
                WITH [i IN range(0, size(ns)-3, 2) |
                    {
                        actor1: ns[i].name,
                        character1: rels[i].character,
                        film: ns[i+1].title + ' (' + coalesce(ns[i+1].year, '') + ')',
                        actor2: ns[i+2].name,
                        character2: rels[i+1].character
                    }
                ] AS path_steps
                RETURN size(path_steps) AS bacon_number, path_steps
                LIMIT 1
                """,
                {"actorA": actor_a_lc, "actorB": actor_b_lc},
            )
            record = result.single()
            if record is None or record["bacon_number"] is None:
                return jsonify({"error": "No path found"}), 404
            return jsonify(
                {"bacon_number": record["bacon_number"], "path": record["path_steps"]}
            )
    except ServiceUnavailable as e:
        logger.error("Database connection failed: %s", e)
        return jsonify({"error": "Database connection failed"}), 503
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        return jsonify({"error": "Unexpected server error"}), 500
