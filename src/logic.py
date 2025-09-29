from src.db import (
    db_add_user, db_get_users, db_update_user, db_delete_user,
    db_add_product, db_get_products, db_update_product, db_delete_product,
    db_add_price_history, db_get_price_history, db_get_products_by_name
)
from datetime import datetime
import random

# ---------------- USERS ---------------- #
class UserManager:
    @staticmethod
    def add_user(first_name, last_name, email, mobile_no, password_hash):
        try:
            data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "mobile_no": mobile_no,
                "password_hash": password_hash   # ✅ fixed here
            }
            res = db_add_user(data)
            if res and hasattr(res, "data") and res.data:
                return {"Success": True, "Message": "User created", "data": res.data[0]}
            return {"Success": False, "Message": "Failed to create user"}
        except Exception as e:
            return {"Success": False, "Message": str(e)}

    @staticmethod
    def get_users():
        # db_get_users already returns a list
        return db_get_users()

    @staticmethod
    def update_user(uid, updates):
        res = db_update_user(uid, updates)
        return res.data if hasattr(res, "data") else res

    @staticmethod
    def delete_user(uid):
        res = db_delete_user(uid)
        return res.data if hasattr(res, "data") else res

# ---------------- PRODUCTS ---------------- #
class ProductManager:
    @staticmethod
    def add_product(user_id, url, name=None, category=None, desired_price=None):
        try:
            data = {
                "user_id": user_id,
                "url": url,
                "name": name,
                "category": category,
                "desired_price": desired_price,
                "last_price": None,
                "last_checked": datetime.utcnow().isoformat()
            }
            res = db_add_product(data)
            if res and hasattr(res, "data") and res.data:
                return {"Success": True, "Message": "Product added", "data": res.data[0]}
            return {"Success": False, "Message": "Failed to add product"}
        except Exception as e:
            return {"Success": False, "Message": str(e)}

    @staticmethod
    def get_products(user_id=None):
        res = db_get_products(user_id)
        return res.data if hasattr(res, "data") else res

    @staticmethod
    def get_products_by_name(name):
        res = db_get_products_by_name(name)
        return res.data if hasattr(res, "data") else res

    @staticmethod
    def update_product(pid, updates):
        updates["last_checked"] = datetime.utcnow().isoformat()
        res = db_update_product(pid, updates)
        return res.data if hasattr(res, "data") else res

    @staticmethod
    def delete_product(pid):
        res = db_delete_product(pid)
        return res.data if hasattr(res, "data") else res

# ---------------- PRICE TRACKING ---------------- #
def fetch_real_time_price(url):
    """Simulate fetching price from a site"""
    # In real scenario, integrate API here
    return round(random.uniform(100, 1000), 2), random.choice(["Amazon", "Flipkart", "Snapdeal"])

def check_and_update_all_products():
    products = db_get_products()
    results = []
    for p in products.data:
        last_price, site = fetch_real_time_price(p["url"])
        last_checked = datetime.utcnow().isoformat()
        # Update product
        ProductManager.update_product(p["pid"], {"last_price": last_price})
        # Save history (only columns that exist in DB)
        db_add_price_history({
            "product_id": p["pid"],
            "price": last_price,
            "checked_at": last_checked
        })
        # Keep site in results for frontend display
        results.append({
            "pid": p["pid"],
            "name": p["name"],
            "lowest_price": last_price,
            "site": site,
            "url": p["url"],
            "last_checked": last_checked
        })
    return results

def track_product_by_name(name):
    products = ProductManager.get_products_by_name(name)
    results = []
    for p in products:
        last_price, site = fetch_real_time_price(p["url"])
        last_checked = datetime.utcnow().isoformat()
        ProductManager.update_product(p["pid"], {"last_price": last_price})
        db_add_price_history({
            "product_id": p["pid"],
            "price": last_price,
            "checked_at": last_checked
        })
        results.append({
            "pid": p["pid"],
            "name": p["name"],
            "lowest_price": last_price,
            "site": site,
            "url": p["url"],
            "last_checked": last_checked
        })
    return results
