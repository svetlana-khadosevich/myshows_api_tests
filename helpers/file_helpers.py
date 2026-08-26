from pathlib import Path
import yaml

def load_sql(filename: str):
    sql_path=Path(__file__).parent.parent / 'data' / filename
    with sql_path.open(mode="r", encoding="utf-8") as file:
        return file.read()


def load_yaml(filename: str) -> dict:
    path = Path(__file__).parent.parent / 'schemas' / filename
    with path.open(mode="r", encoding="utf-8") as file:
        return yaml.safe_load(file)
