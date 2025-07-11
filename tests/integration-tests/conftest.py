import pytest
from baconometer.app import create_app

# TODO: use config file instead?
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4jtest123"


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def app():
    """
    Create Flask app connected to test DB.
    """
    app = create_app(
        {
            "TESTING": True,
            "NEO4J_URI": NEO4J_URI,
            "NEO4J_USER": NEO4J_USER,
            "NEO4J_PASSWORD": NEO4J_PASSWORD,
        }
    )

    return app
