import allure
import psycopg
import pytest
import requests

from psycopg.rows import dict_row

from config.api_config import CONN_PARAMS
from helpers.add_data_functions import add_series, delete_series, add_series_for_put, delete_series_for_put
from helpers.api_helpers import ApiSession


@pytest.fixture(scope="session")
def api_session():
    with allure.step("Создаём API-сессию"):
        myshows_session=requests.Session()
        yield ApiSession(myshows_session)
        with allure.step("Закрываем API-сессию"):
            myshows_session.close()


@pytest.fixture()
def series_data():
    with psycopg.connect(**CONN_PARAMS, row_factory=dict_row) as conn:
        add_series(conn, "add_series.sql")
        yield series_data
        delete_series(conn)


@pytest.fixture()
def series_data_put():
    with psycopg.connect(**CONN_PARAMS, row_factory=dict_row) as conn:
        series_id = add_series_for_put(conn)
        yield series_id
        delete_series_for_put(conn, series_id)


@pytest.fixture()
def series_data_get(request):
    file = request.param
    with psycopg.connect(**CONN_PARAMS, row_factory=dict_row) as conn:
        if file is not None:
            add_series(conn, file)
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS number FROM series")
            row = cur.fetchone()
            number = row["number"]
        yield number
        delete_series(conn)
