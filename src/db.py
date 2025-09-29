from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# ---------------- USER CRUD ---------------- #
def db_add_user(data):
    return supabase.table("users").insert(data).execute()

def db_get_users():
    # also fetch products for PID display
    users = supabase.table("users").select("*").execute()
    products = supabase.table("products_price").select("*").execute()
    user_list = []
    for u in users.data:
        u_products = [p for p in products.data if p['user_id'] == u['uid']]
        u['products'] = u_products
        user_list.append(u)
    return user_list

def db_update_user(uid, updates):
    return supabase.table("users").update(updates).eq("uid", uid).execute()

def db_delete_user(uid):
    return supabase.table("users").delete().eq("uid", uid).execute()

# ---------------- PRODUCT CRUD ---------------- #
def db_add_product(data):
    return supabase.table("products_price").insert(data).execute()

def db_get_products(user_id=None):
    query = supabase.table("products_price").select("*")
    if user_id:
        query = query.eq("user_id", user_id)
    return query.execute()

def db_update_product(pid, updates):
    return supabase.table("products_price").update(updates).eq("pid", pid).execute()

def db_delete_product(pid):
    return supabase.table("products_price").delete().eq("pid", pid).execute()

# ---------------- PRICE HISTORY ---------------- #
def db_add_price_history(data):
    # data: {"product_id":..., "price":..., "checked_at":...}
    return supabase.table("price_history").insert(data).execute()

def db_get_price_history(product_id):
    return supabase.table("price_history").select("*").eq("product_id", product_id).execute()

# ---------------- GET PRODUCTS BY NAME ---------------- #
def db_get_products_by_name(name):
    return supabase.table("products_price").select("*").ilike("name", f"%{name}%").execute()
