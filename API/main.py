# main.py
# Frontend -> API -> logic -> db -> supabase(response)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

# Import UserManager & ProductManager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import UserManager, ProductManager

# ------------------------------- App Setup -----------------------------------------
app = FastAPI(title="E-commerce Product Price Tracker", version="1.0")

# ----------------------------Allow frontend (Streamlit/React) to call the API --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------- Business Logic Instances ----------------------
user_manager = UserManager()
product_manager = ProductManager()

# ------------------ Data Models ------------------------------------
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    mobile_no: int
    password_hash: str

class UserUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    email: str = None
    mobile_no: int = None
    password_hash: str = None

class ProductCreate(BaseModel):
    user_id: int
    url: str
    desired_price: float

class ProductUpdate(BaseModel):
    url: str = None
    desired_price: float = None
    name: str = None
    category: str = None
    last_price: float = None

# ----------------------- Endpoints ---------------------------------
@app.get("/")
def home():
    return {"message": "E-commerce Product Price Tracker is running!"}

# ---------------------- Users CRUD ----------------------
@app.get("/users")
def get_users():
    return user_manager.get_users()

@app.post("/users")
def create_user(user: UserCreate):
    result = user_manager.add_user(
        user.first_name, user.last_name, user.email, user.mobile_no, user.password_hash
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.put("/users/{uid}")
def update_user(uid: int, user: UserUpdate):
    updated_fields = {k: v for k, v in user.dict().items() if v is not None}
    result = user_manager.update_user(uid, updated_fields)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.delete("/users/{uid}")
def delete_user(uid: int):
    result = user_manager.delete_user(uid)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

# ---------------------- Products CRUD ----------------------
@app.get("/products_price")
def get_products():
    return product_manager.get_products()

@app.post("/products_price")
def create_product(product: ProductCreate):
    result = product_manager.add_product(
        user_id=product.user_id,
        url=product.url,
        desired_price=product.desired_price
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.put("/products_price/{pid}")
def update_product(pid: int, product: ProductUpdate):
    updated_fields = {k: v for k, v in product.dict().items() if v is not None}
    result = product_manager.update_product(pid, updated_fields)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.delete("/products_price/{pid}")
def delete_product(pid: int):
    result = product_manager.delete_product(pid)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

# ---------------------- Run App ---------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
