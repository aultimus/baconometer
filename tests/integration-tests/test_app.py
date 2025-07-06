def test_bacon_number_kevin_bacon_to_self(client):
    response = client.get("/bacon-number/Kevin%20Bacon/Kevin%20Bacon")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    expected = {"bacon_number": 0, "path": []}
    assert response.get_json() == expected, f"Unexpected body: {response.get_json()}"


import pytest

@pytest.mark.parametrize("actor_a,actor_b,expected_status,expected_body", [
    ("foo" * 40, "Kevin Bacon", 400, {"error": "Input data too long"}),  # actorA too long
    ("Kevin Bacon", "foo" * 40, 400, {"error": "Input data too long"}),  # actorB too long
    ("foo" * 40, "bar" * 40, 400, {"error": "Input data too long"}),     # both too long
    ("Kevin Bacon", "Tom Hanks", 200, None),                               # both valid (control)
])
def test_long_input_variants(client, actor_a, actor_b, expected_status, expected_body):
    response = client.get(f"/bacon-number/{actor_a}/{actor_b}")
    assert response.status_code == expected_status, f"Unexpected status code: {response.status_code}"
    if expected_body is not None:
        assert response.get_json() == expected_body, f"Unexpected body: {response.get_json()}"
    elif expected_status == 200:
        # In the control case, we don't know the actual bacon number/path, but it should be a dict
        assert isinstance(response.get_json(), dict)
