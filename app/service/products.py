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


def save_products(products:List[dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

def add_product(product: dict) -> dict:
    products = get_all_products()

    if any(p["sku"] == product["sku"] for p in products):
        raise HTTPException(status_code=400, detail=f"Product with SKU {products['sku']} already exists")


    products.append(product)
    save_products(products)
    return product


def delete_product(id: str) -> str:
    products = get_all_products()

    for idx, p in enumerate(products):
        if p["id"] == str(id):
            deleted = products.pop(idx)
            save_products(products)
            return f"Product with SKU {deleted['sku']} deleted successfully"

    raise ValueError(f"Product with ID '{id}' not found")


def update_product(id: str, updated_data: dict) -> dict:
    products = get_all_products()

    for p in products:
        if p["id"] == str(id):
            p.update(updated_data)
            save_products(products)
            return p

    raise ValueError(f"Product with ID '{id}' not found")
