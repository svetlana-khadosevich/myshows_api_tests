from http import HTTPStatus

import pytest
import requests
import psycopg
from psycopg.rows import dict_row
from jsonschema import validate

from config.api_config import CONN_PARAMS, BASE_URL
from helpers.file_helpers import load_yaml


class TestGetSeries:
    '''Тесты на проверку метода GET/series'''
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

# Спринт 11.3
# Задание 2.Параметризация фикстуры
    @pytest.mark.parametrize(
        "series_data_get",
        [
            None,
            "add_1_series.sql",
            "add_3_series.sql",
        ],
        indirect=True)
    def test_get_series(self, series_data_get):
        response = requests.get(
                   BASE_URL + "/series"
        )
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        number = series_data_get  # получаем из фикстуры количество строк, добавленных в БД
        assert len(body) == number
        template = load_yaml("GetSeries.yml")
        validate(body, template)


# Спринт 11.3
# Задание 1.Параметризация теста
class TestPutSeries:
    '''Параметризация теста PUT/series'''
    @pytest.mark.parametrize(
        "field_name, new_value",
        [
            ("name", "Обновленное название"),
            ("photo", "https://example.com/updated.jpg"),
            ("rating", 9),
            ("status", "will_watch"),
            ("review", "Новая заметка"),
        ])
    def test__put_series(self, series_data_put, field_name, new_value):
        series_id = series_data_put
        payload = {"name": "Новое имя",
                   "photo": "https://example.com/test.jpg",
                   "rating": 7,
                   "status": "watching",
                   "review": "Новая заметка"}
        payload[field_name] = new_value
        response = requests.put(
                   BASE_URL + "/series/" + str(series_id),
                   json=payload
                               )
        assert response.status_code == HTTPStatus.OK
        with psycopg.connect(**CONN_PARAMS, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT * FROM series WHERE id = %s""", (series_id,))
                row = cur.fetchone()
                assert row[field_name] == new_value
