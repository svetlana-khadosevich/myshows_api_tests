import requests

from config.api_config import BASE_URL
from fixtures.api_fixtures import series_data

from http import HTTPStatus

class TestGetSeries:
    def test__get_series_by_rating(self, series_data):
        response = requests.get(
                   BASE_URL + "/series",
                   params={"rating": 7}
                   )
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        for series in body:
            assert series["rating"] == 7

    def test_get_series_by_status(self, series_data):
        response = requests.get(
                   BASE_URL + "/series",
                   params={"status": "watched"}
        )
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        for series in body:
            assert series["status"] == "watched"

    def test_get_series_by_id_desc(self, series_data):
        response = requests.get(
                   BASE_URL + "/series",
                   params={"sort": "id_desc"}
        )
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        for series in range(len(body) - 1):
            assert body[series]["id"] > body[series + 1]["id"]

    def test_get_series_by_id_asc(self, series_data):
        response = requests.get(
                   BASE_URL + "/series",
                   params={"sort": "id_asc"}
        )
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        for series in range(len(body) - 1):
            assert body[series]["id"] < body[series + 1]["id"]




