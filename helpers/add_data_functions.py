from helpers.file_helpers import load_sql

def add_series(conn):
    with conn.cursor() as cur:
        cur.execute(load_sql("add_series.sql"))
        conn.commit()

def delete_series(conn):
    with conn.cursor() as cur:
        cur.execute(load_sql("delete_series.sql"))
        conn.commit()