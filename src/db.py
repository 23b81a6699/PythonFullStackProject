# db.py

import os
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

# --------------------------
# Users Table Operations
# --------------------------
def create_user(first_name, last_name, email, mobile_no, password_hash):
    return supabase.table("users").insert({
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "mobile_no": mobile_no,
        "password_hash": password_hash,
        "created_at": datetime.now()
    }).execute()

def get_all_users():
    return supabase.table("users").select("*").order("created_at").execute()

def update_user(uid, new_user: dict):
    return supabase.table("users").update(new_user).eq("uid", uid).execute()

def delete_user(uid):
    return supabase.table("users").delete().eq("uid", uid).execute()

# --------------------------
# Products Table Operations
# --------------------------
def create_product(user_id, url, name=None, category=None, last_price=None, desired_price=None):
    return supabase.table("products_price").insert({
        "user_id": user_id,
        "url": url,
        "name": name,
        "category": category,
        "last_price": last_price,
        "desired_price": desired_price,
        "last_checked": datetime.now()
    }).execute()

def get_all_products():
    return supabase.table("products_price").select("*").order("name").execute()

def update_product(pid, updated_fields: dict):
    return supabase.table("products_price").update(updated_fields).eq("pid", pid).execute()

def delete_product(pid):
    return supabase.table("products_price").delete().eq("pid", pid).execute()
