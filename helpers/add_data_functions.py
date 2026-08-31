from helpers.file_helpers import load_sql


def add_series(conn, file):
    with conn.cursor() as cur:
        cur.execute(load_sql(file))
        conn.commit()


def delete_series(conn):
    with conn.cursor() as cur:
        cur.execute(load_sql("delete_series.sql"))
        conn.commit()


def add_series_for_put(conn):
    with conn.cursor() as cur:
        cur.execute(load_sql("add_data_for_put.sql"))
        conn.commit()
        row = cur.fetchone()
        series_id = row["id"]
        return series_id


def delete_series_for_put(conn, series_id):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM series where id = %s""", (series_id,))
        conn.commit()
