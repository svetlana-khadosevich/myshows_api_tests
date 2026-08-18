from pathlib import Path

def load_sql(filename: str):
    sql_path=Path(__file__).parent.parent / 'data' / filename
    with sql_path.open(mode="r", encoding="utf-8") as file:
        return file.read()
