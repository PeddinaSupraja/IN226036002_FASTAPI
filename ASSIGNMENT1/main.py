from fastapi import FastAPI , Query
app = FastAPI()
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, 'category': 'Electronics','in_stock': True},
    {"id": 2, "name": "Notebook", "price": 99, 'category': 'Stationery','in_stock': True},
    {"id": 3, "name": "USB Hub", "price": 799, 'category': 'Electronics','in_stock': False},
    {"id": 4, "name": "Pen Set", "price": 49, 'category': 'Stationery','in_stock': True},
    {"id": 5, "name": "Bluetooth Speaker", "price": 1499, 'category': 'Electronics','in_stock': True},
    {"id": 6, "name": "Sofa", "price": 7999, 'category': 'Furniture','in_stock': False},
    {"id": 7, "name": "Wooden Table", "price": 1999, 'category': 'Furniture','in_stock': True},
]
@app.get("/")
def home():
    return {"message": "Welcome to the E-Commerce API!"}
@app.get("/products")
def get_all_products():
    return {"products": products, "total": len(products)}
@app.get("/products/in-stock")
def get_in_stock_products():
    in_stock_products = [p for p in products if p["in_stock"]]
    return {"products": in_stock_products, "total": len(in_stock_products)}
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {"product": product}
    return {"error": "Product not found"}
@app.get("/products/category/{category}")
def get_products_by_category(category: str):
    filtered = [p for p in products if p["category"].lower() == category.lower()]
    return {"category": category, "products": filtered, "total": len(filtered)}
@app.get("/store/summary")
def store_summary():
    total = len(products)
    in_stock = sum(1 for p in products if p["in_stock"])
    out_of_stock = total - in_stock
    categories = sorted({p["category"] for p in products})
    return {
        "total_products": total,
        "in_stock_count": in_stock,
        "out_of_stock_count": out_of_stock,
        "categories": categories,
    }
@app.get("/products/search/{keyword}")
def search_products_by_keyword(keyword: str):
    matched = [p for p in products if keyword.lower() in p["name"].lower()]
    if not matched:
        return {"message": "No products matched your search"}
    return {"keyword": keyword, "products": matched, "total": len(matched)}