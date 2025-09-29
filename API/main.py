from fastapi import FastAPI, HTTPException
from src.logic import UserManager, ProductManager, check_and_update_all_products, track_product_by_name

app = FastAPI()

# ---------------- USERS ---------------- #
@app.post("/users/")
def create_user(user: dict):
    res = UserManager.add_user(
        user.get("first_name"), user.get("last_name"),
        user.get("email"), user.get("mobile_no"),
        user.get("password")
    )
    if not res["Success"]:
        raise HTTPException(status_code=400, detail=res["Message"])
    return res

@app.get("/users/")
def list_users():
    return UserManager.get_users()

@app.put("/users/{uid}")
def update_user(uid: int, updates: dict):
    return UserManager.update_user(uid, updates)

@app.delete("/users/{uid}")
def delete_user(uid: int):
    return UserManager.delete_user(uid)

# ---------------- PRODUCTS ---------------- #
@app.post("/products/")
def create_product(product: dict):
    res = ProductManager.add_product(
        product.get("user_id"), product.get("url"),
        product.get("name"), product.get("category"),
        product.get("desired_price")
    )
    if not res["Success"]:
        raise HTTPException(status_code=400, detail=res["Message"])
    return res

@app.get("/products/")
def list_products(user_id: int = None):
    return ProductManager.get_products(user_id)

# ---------------- TRACKING ---------------- #
@app.post("/track/")
def track_all_products():
    try:
        tracked = check_and_update_all_products()
        return tracked
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Updated: use query parameter instead of path parameter
@app.get("/track/")
def track_by_name(name: str):
    tracked = track_product_by_name(name)
    if not tracked:
        raise HTTPException(status_code=404, detail="Not Found")
    return {"Products": tracked}
