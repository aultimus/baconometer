def test_bacon_number_kevin_bacon_to_self(client):
    response = client.get("/bacon-number/Kevin%20Bacon/Kevin%20Bacon")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    expected = {"bacon_number": 0, "path": []}
    assert response.get_json() == expected, f"Unexpected body: {response.get_json()}"
