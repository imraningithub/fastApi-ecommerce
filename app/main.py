from fastapi import FastAPI, HTTPException, Query, Path
from service.products import get_all_products, add_product, delete_product, update_product
from schema.product import Product
from uuid import uuid4, UUID
from datetime import datetime

app = FastAPI()


# Static Method
@app.get('/')
def root():
    return {'message':"Welcome to Backend world"}



# Dynamic Method

@app.get("/products")
def list_products(
    name: str = Query(default=None, 
    min_length= 1, 
    max_length=50, 
    description= "Search By Product Name(case insesnsitive)"),

    sort_by_price: bool = Query(default=False, description="Sort product by price"),

    order: str = Query(default="asc", description="Sort order when sort_by_price= True (asc, desc)"),

    limit: int = Query(default= 10, ge=1, le=100, description="Number of products"),

    offset: int = Query(default=0, description="Page Number")
    
):


    products = get_all_products()

    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]

    if not products:
            raise HTTPException(
                status_code=404, detail= f"No product found matching name={name} "
            )

    if sort_by_price:
        reversed = order == "desc"
        products = sorted(products, key=lambda p:p.get("price", 0), reverse=reversed)        

    total = len(products)
    products = products[offset:offset + limit]

    return {"total" : total, "limit": limit, "items": products}
    
@app.get("/products/{product_id}")
def get_product_by_id(product_id: str = Path(
    ..., 
    min_length= 36, 
    max_length=36,
    description="Product ID",
    example="12345678-1234-1234-1234-123456789012"
)):
    products = get_all_products()
    for product in products:
        if product['id'] == product_id:
            return product
    
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/products/{product_id}")
def delete_product_by_id(product_id: UUID = Path(
    ...,
    description="Product UUID",
    example= "UUID"
)):
    try:
        res = delete_product(str(product_id))
        return res

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))        







@app.post("/products", status_code=201)
def create_product(product: Product):
    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.utcnow().isoformat() + "Z"

    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


    return product.model_dump(mode="json")


# ✅ Route Handler for PUT /products/{product_id}
@app.put("/products/{product_id}")
def update_product_by_id(
    payload: Product,
    product_id: UUID = Path(..., description="Product UUID"),
):
    try:
        updated = update_product(str(product_id), payload.model_dump(mode="json", exclude_unset=True))
        return updated
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

  


            
    

