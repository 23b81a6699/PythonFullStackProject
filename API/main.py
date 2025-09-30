from fastapi import FastAPI, HTTPException, Query
from src.logic import UserManager, ProductManager, check_and_update_all_products, track_product_by_name

app = FastAPI()

# Create instances of managers
user_manager = UserManager()
product_manager = ProductManager()

# ---------------- USERS ---------------- #
@app.post("/users/")
def create_user(user: dict):
    res = user_manager.add_user(
        user.get("first_name"), user.get("last_name"),
        user.get("email"), user.get("mobile_no"),
        user.get("password")
    )
    if not res["Success"]:
        raise HTTPException(status_code=400, detail=res["Message"])
    return res

@app.get("/users/")
def list_users():
    return user_manager.get_users()

@app.put("/users/{uid}")
def update_user(uid: int, updates: dict):
    return user_manager.update_user(uid, updates)

@app.delete("/users/{uid}")
def delete_user(uid: int):
    return user_manager.delete_user(uid)

# ---------------- PRODUCTS ---------------- #
@app.post("/products/")
def create_product(product: dict):
    res = product_manager.add_product(
        user_id=product.get("user_id"),
        url=product.get("url"),
        desired_price=product.get("desired_price"),
        name=product.get("name"),
        category=product.get("category")
    )
    if not res["Success"]:
        raise HTTPException(status_code=400, detail=res["Message"])
    return res

@app.get("/products/")
def list_products(user_id: int = Query(None, description="Filter by user_id")):
    return product_manager.get_products(user_id)

# ---------------- TRACKING ---------------- #
@app.post("/track/")
def track_all_products():
    try:
        tracked, all_products = check_and_update_all_products()
        return {"Products": all_products, "Alerts": tracked}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/track/")
def track_by_name(name: str = Query(..., description="Product name to search")):
    tracked = track_product_by_name(name)
    if not tracked:
        raise HTTPException(status_code=404, detail="No matching product found")
    return {"Products": tracked}
