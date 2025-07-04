import pytest
from app import app as flask_app

# These tests largely duplicate the system tests, but they are run in-process
# and do not require the Docker container to be running.
# These are mostly here for demonstration purposes


@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client


def test_bacon_number_kevin_bacon_to_self(client):
    response = client.get("/bacon-number/Kevin%20Bacon/Kevin%20Bacon")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    expected = {"bacon_number": 0, "path": []}
    assert response.get_json() == expected, f"Unexpected body: {response.get_json()}"
