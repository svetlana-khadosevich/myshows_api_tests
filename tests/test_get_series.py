from http import HTTPStatus

import allure
import pytest
import psycopg
from psycopg.rows import dict_row
from jsonschema import validate

from config.api_config import CONN_PARAMS, BASE_URL
from helpers.file_helpers import load_yaml

@allure.suite("Тесты на метод GET/series")
class TestGetSeries:
    @allure.title("Вывод сериалов с рейтингом 7")
    def test__get_series_by_rating(self, series_data, api_session):
        response = api_session.get(
                   BASE_URL + "/series",
                   params={"rating": 7}
                               )

        with allure.step("Проверяем статус код"):
            assert response.status_code == HTTPStatus.OK
        body = response.json()
        with allure.step("Проверяем рейтинг сериалов в списке"):
            for series in body:
                assert series["rating"] == 7

    @allure.title("Вывод сериалов в статусе 'просмотрено'")
    def test_get_series_by_status(self, series_data, api_session):
        response = api_session.get(
                   BASE_URL + "/series",
                   params={"status": "watched"}
        )
        with allure.step("Проверяем статус код"):
            assert response.status_code == HTTPStatus.OK
        body = response.json()
        with allure.step("Проверяем статус сериалов в теле ответа"):
            for series in body:
                assert series["status"] == "watched"

    @allure.title("Вывод сериалов в порядке убывания id")
    def test_get_series_by_id_desc(self, series_data, api_session):
        response = api_session.get(
                   BASE_URL + "/series",
                   params={"sort": "id_desc"}
        )
        with allure.step("Проверяем статус код"):
            assert response.status_code == HTTPStatus.OK
        body = response.json()
        with allure.step("Проверяем сортировку"):
            for series in range(len(body) - 1):
                assert body[series]["id"] > body[series + 1]["id"]

    @allure.title("Вывод сериалов в порядке возрастания id")
    def test_get_series_by_id_asc(self, series_data, api_session):
        response = api_session.get(
                   BASE_URL + "/series",
                   params={"sort": "id_asc"}
        )
        with allure.step("Проверяем статус код"):
            assert response.status_code == HTTPStatus.OK
        body = response.json()
        with allure.step("Проверяем сортировку"):
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
    @allure.title("Проверка схемы ответа")
    def test_get_series(self, series_data_get, api_session):
        response = api_session.get(
                   BASE_URL + "/series"
        )
        with allure.step("Проверяем статус код"):
            assert response.status_code == HTTPStatus.OK
        body = response.json()
        number = series_data_get  # получаем из фикстуры количество строк, добавленных в БД
        with allure.step("Проверяем количество добавленных строк в БД"):
            assert len(body) == number
        template = load_yaml("GetSeries.yml")
        validate(body, template)


# Спринт 11.3
# Задание 1.Параметризация теста
@allure.suite("Тесты на метод PUT/series")
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
    @allure.title("Редактирование поля {field_name}")
    def test__put_series(self, series_data_put, api_session, field_name, new_value):
        series_id = series_data_put
        payload = {"name": "Новое имя",
                   "photo": "https://example.com/test.jpg",
                   "rating": 7,
                   "status": "watching",
                   "review": "Новая заметка"}
        payload[field_name] = new_value
        response = api_session.put(
                   BASE_URL + "/series/" + str(series_id),
                   json=payload
                               )
        with allure.step("Проверяем код ответа"):
            assert response.status_code == HTTPStatus.OK
        with psycopg.connect(**CONN_PARAMS, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT * FROM series WHERE id = %s""", (series_id,))
                row = cur.fetchone()
                with allure.step("Проверяем изменение в БД"):
                    assert row[field_name] == new_value
