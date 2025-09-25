# logic.py
from db import (
    create_user, get_all_users, update_user, delete_user,
    create_product, get_all_products, update_product, delete_product
)
from datetime import datetime
import requests
from bs4 import BeautifulSoup


# -------------------------------------------------------------------------
#                              User Manager
# --------------------------------------------------------------------------

class UserManager:
    # ---- CREATE ----
    def add_user(self, first_name, last_name, email, mobile_no, password_hash):
        if not all([first_name, last_name, email, mobile_no, password_hash]):
            return {"Success": False, "Message": "All fields are required."}
        result = create_user(first_name, last_name, email, mobile_no, password_hash)
        if result.data:
            return {"Success": True, "Message": "User added successfully!"}
        return {"Success": False, "Message": f"Error: {result.error}"}

    # ---- READ ----
    def get_users(self):
        return get_all_users()

    # ---- UPDATE ----
    def update_user(self, uid, updated_fields: dict):
        if not updated_fields:
            return {"Success": False, "Message": "No fields provided for update."}
        result = update_user(uid, updated_fields)
        if result.data:
            return {"Success": True, "Message": "User updated successfully!"}
        return {"Success": False, "Message": f"Error: {result.error}"}

    # ---- DELETE ----
    def delete_user(self, uid):
        result = delete_user(uid)
        if result.data:
            return {"Success": True, "Message": "User deleted successfully!"}
        return {"Success": False, "Message": f"Error: {result.error}"}


# -------------------------------------------------------------------------
#                                     Product price
# --------------------------------------------------------------------------

class ProductManager:
    # ---- HELPER: Fetch product info from URL ----
    def fetch_product_details(self, url):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Example: Extract name, category, last_price from HTML
            # You may need to customize selectors based on the website
            name = soup.find("span", {"id": "productTitle"}).get_text(strip=True) if soup.find("span", {"id": "productTitle"}) else "Unknown"
            category = soup.find("a", {"class": "a-link-normal a-color-tertiary"}).get_text(strip=True) if soup.find("a", {"class": "a-link-normal a-color-tertiary"}) else "General"
            price_tag = soup.find("span", {"id": "priceblock_ourprice"}) or soup.find("span", {"id": "priceblock_dealprice"})
            last_price = float(price_tag.get_text(strip=True).replace("₹","").replace(",","")) if price_tag else None

            return name, category, last_price
        except Exception as e:
            return "Unknown", "General", None

    # ---- CREATE ----
    def add_product(self, user_id, url, desired_price):
        if not url or desired_price is None:
            return {"Success": False, "Message": "URL and Desired Price are required."}

        # Automatically fetch product details
        name, category, last_price = self.fetch_product_details(url)

        result = create_product(user_id, url, name, category, last_price, desired_price)
        if result.data:
            return {"Success": True, "Message": "Product added successfully!"}
        return {"Success": False, "Message": f"Error: {result.error}"}

    # ---- READ ----
    def get_products(self):
        return get_all_products()

    # ---- UPDATE ----
    def update_product(self, pid, updated_fields: dict):
        if not updated_fields:
            return {"Success": False, "Message": "No fields provided for update."}
        updated_fields["last_checked"] = datetime.now()
        result = update_product(pid, updated_fields)
        if result.data:
            return {"Success": True, "Message": "Product updated successfully!"}
        return {"Success": False, "Message": f"Error: {result.error}"}

    # ---- DELETE ----
    def delete_product(self, pid):
        result = delete_product(pid)
        if result.data:
            return {"Success": True, "Message": "Product deleted successfully!"}
        return {"Success": False, "Message": f"Error: {result.error}"}

