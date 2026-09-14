import json
from pathlib import Path
from typing import List, Dict


DATA_FILE = Path(__file__).parent.parent / "Data" / "products.json"

def load_products() -> List[dict]:
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_products() -> List[dict]:
    return load_products()        