import psycopg
import pytest

from config.api_config import CONN_PARAMS
from helpers.add_data_functions import add_series
from helpers.add_data_functions import delete_series
from psycopg.rows import dict_row

@pytest.fixture()
def series_data():
    with psycopg.connect(**CONN_PARAMS, row_factory=dict_row) as conn:
        add_series(conn)
        yield
        delete_series(conn)

