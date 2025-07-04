import requests

BASE_URL = "http://localhost:5000"


def test_bacon_number_kevin_bacon_to_self():
    response = requests.get(f"{BASE_URL}/bacon-number/Kevin%20Bacon/Kevin%20Bacon")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    expected = {"bacon_number": 0, "path": []}
    assert response.json() == expected, f"Unexpected body: {response.json()}"


# This test could be flaky if we return another path, but it is a good sanity
# check that the API is working and returns a valid path.
def test_bacon_number_kevin_bacon_to_tom_hanks():
    response = requests.get(f"{BASE_URL}/bacon-number/Kevin%20Bacon/Tom%20Hanks")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    actual_bacon_number = response.json().get("bacon_number")
    assert actual_bacon_number == 1, f"Unexpected bacon number: {actual_bacon_number}"


# This test could be flaky if we return another path, but it is a good sanity
# check that the API is working and returns a valid path.
def test_path_kevin_bacon_to_tom_hanks():
    response = requests.get(f"{BASE_URL}/bacon-number/Kevin%20Bacon/Tom%20Hanks")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    expected = {
        "bacon_number": 1,
        "path": [
            {
                "actor1": "Kevin Bacon",
                "actor1_url": "https://www.themoviedb.org/person/4724",
                "actor2": "Tom Hanks",
                "actor2_url": "https://www.themoviedb.org/person/31",
                "character1": "Robert Sherrod",
                "character2": "Narrator",
                "film": "Beyond All Boundaries (2009)",
                "film_url": "https://www.themoviedb.org/movie/574379",
            }
        ],
    }
    assert response.json() == expected, f"Unexpected body: {response.json()}"
