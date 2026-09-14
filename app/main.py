from fastapi import FastAPI, HTTPException, Query
from service.products import get_all_products

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
    