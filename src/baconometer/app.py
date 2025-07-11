from re import A
from .config import Config
from flask import current_app, Flask, render_template, jsonify
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging
from dataclasses import asdict, dataclass

from flask import Blueprint

bp = Blueprint("main", __name__)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        # load default config from file or env
        app.config.from_object(Config)
    else:
        # use explicitly provided config
        app.config.from_mapping(
            test_config,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )
    print("DB URI:", app.config["NEO4J_URI"])

    # Neo4j connection setup
    app.driver = GraphDatabase.driver(
        app.config["NEO4J_URI"],
        auth=(app.config["NEO4J_USER"], app.config["NEO4J_PASSWORD"]),
    )

    # register_extensions(app)
    app.register_blueprint(bp)

    return app


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FilmStepResponse:
    film_url: str
    film: str
    actor1: str
    character1: str
    actor1_url: str
    actor2: str
    character2: str
    actor2_url: str

    @classmethod
    def from_db(cls, db_row):
        return cls(
            film_url=f"https://www.themoviedb.org/movie/{db_row['film_id']}",
            film=db_row["film"],
            actor1=db_row["actor1"],
            character1=db_row["character1"],
            actor1_url=f"https://www.themoviedb.org/person/{db_row['actor1_id']}",
            actor2=db_row["actor2"],
            actor2_url=f"https://www.themoviedb.org/person/{db_row['actor2_id']}",
            character2=db_row["character2"],
        )


@bp.route("/")
def baconify():
    return render_template("baconify.html")


"""
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
"""


@bp.route("/bacon-number/<actorA>/<actorB>")
def bacon_number(actorA, actorB):
    """
    Given two actor names, compute the Bacon number and the path of films
    that connect the two actors.

    The Bacon number is the number of films in the shortest path between
    the two actors, where each film is a hop.

    The path is returned as a list of dictionaries, each containing
    information about a hop in the path.

    If an error occurs, the function returns a JSON response with an error message
    and a status code.

    If no path is found, a 404 error is returned.

    If the database connection fails, a 503 error is returned.

    If any other unexpected error occurs, a 500 error is returned.
    """
    # Convert input names to lowercase for case-insensitive search
    if len(actorA) > 100 or len(actorB) > 100:
        return jsonify({"error": "Input data too long"}), 400

    actor_a_lc = actorA.lower()
    actor_b_lc = actorB.lower()
    if actor_a_lc == actor_b_lc:
        # Return bacon number 0 and a trivial path
        return jsonify({"bacon_number": 0, "path": []})
    try:
        with current_app.driver.session() as session:
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
                        actor1_id: ns[i].nconst,
                        actor1: ns[i].name,
                        character1: rels[i].character,
                        film_id: ns[i+1].tconst,
                        film: ns[i+1].title + ' (' + coalesce(ns[i+1].year, '') + ')',
                        actor2_id: ns[i+2].nconst,
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
            # Convert Neo4j data to clean response type
            path = [
                asdict(FilmStepResponse.from_db(step)) for step in record["path_steps"]
            ]
            return jsonify({"bacon_number": record["bacon_number"], "path": path})
    except ServiceUnavailable as e:
        logger.error("Database connection failed: %s", e)
        return jsonify({"error": "Database connection failed"}), 503
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        return jsonify({"error": "Unexpected server error"}), 500
