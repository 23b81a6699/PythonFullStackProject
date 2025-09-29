import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"

st.set_page_config(page_title="E-commerce Product Price Tracker", layout="centered")
st.title("🛒 E-commerce Product Price Tracker")

menu = [
    "Add User", "Update User", "Delete User",
    "Add Product", "View Products",
    "Track Products", "Track Product by Name", "View Users"
]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- USERS ---------------- #
if choice == "Add User":
    st.subheader("➕ Add User")
    with st.form("add_user"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        mobile_no = st.text_input("Mobile No")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Add User")
        if submitted:
            res = requests.post(f"{API_URL}/users/", json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "mobile_no": mobile_no,
                "password": password
            })
            if res.status_code == 200:
                data = res.json()["data"]
                st.balloons()
                st.success(f"🎉 User added successfully! UID: {data['uid']}, Name: {data['first_name']} {data['last_name']}")
            else:
                st.error(f"Failed: {res.text}")

elif choice == "Update User":
    st.subheader("✏️ Update User")
    uid = st.number_input("User ID", min_value=1)
    new_email = st.text_input("New Email")
    if st.button("Update User", key=f"update_user_{uid}"):
        res = requests.put(f"{API_URL}/users/{uid}", json={"email": new_email})
        if res.status_code == 200:
            st.balloons()
            st.success("🎉✨💥 User updated successfully! 💥✨🎉")
        else:
            st.error(f"Failed: {res.text}")

elif choice == "Delete User":
    st.subheader("🗑️ Delete User")
    uid = st.number_input("User ID", min_value=1)
    if st.button("Delete User", key=f"delete_user_{uid}"):
        res = requests.delete(f"{API_URL}/users/{uid}")
        if res.status_code == 200:
            st.snow()
            st.success("✨🚀 User deleted successfully!")
        else:
            st.error(f"Failed: {res.text}")

# ---------------- PRODUCTS ---------------- #
elif choice == "Add Product":
    st.subheader("➕ Add Product")
    with st.form("add_product"):
        user_id = st.number_input("User ID", min_value=1)
        url = st.text_input("Product URL")
        name = st.text_input("Product Name")
        category = st.text_input("Category")
        desired_price = st.number_input("Desired Price", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Add Product")
        if submitted:
            res = requests.post(f"{API_URL}/products/", json={
                "user_id": user_id,
                "url": url,
                "name": name,
                "category": category,
                "desired_price": desired_price
            })
            if res.status_code == 200:
                data = res.json()["data"]
                st.snow()
                st.success(f"✨🎉 Product added! PID: {data['pid']}, Name: {data['name']}")
            else:
                st.error(f"Failed: {res.text}")

# ---------------- VIEW PRODUCTS ---------------- #
elif choice == "View Products":
    st.subheader("📋 View Products")
    res = requests.get(f"{API_URL}/products/")
    if res.status_code == 200:
        products = res.json()
        if products:
            for product in products:
                with st.expander(f"{product.get('name','N/A')} ,(pid : {product.get('pid','N/A')})"):
                    st.write(f"**User ID:** {product.get('user_id')}")
                    st.write(f"**Product ID:** {product.get('pid')}")
                    st.write(f"**Category:** {product.get('category')}")
                    st.write(f"**Last Price:** {product.get('last_price')}")
                    st.write(f"**Desired Price:** {product.get('desired_price')}")
                    st.write(f"**URL:** {product.get('url')}")
                    st.write(f"**Last Checked:** {product.get('last_checked')}")
        else:
            st.warning("No products found.")
    else:
        st.error(f"Failed: {res.text}")

# ---------------- TRACK PRODUCTS ---------------- #
elif choice == "Track Products":
    st.subheader("📊 Track All Products")
    if st.button("Run Tracker", key="track_all"):
        res = requests.post(f"{API_URL}/track/")
        if res.status_code == 200:
            tracked = res.json()
            for p in tracked:
                with st.expander(f"{p['name']}"):
                    st.write(f"PID : {p.get('pid','N/A')}")
                    st.write(f"**Last Price:** {p['lowest_price']} at {p['site']}")
                    st.write(f"URL: {p['url']}")
                    st.write(f"Last Checked: {p['last_checked']}")
            st.success("🎊✨📈 Tracking completed! 📈✨🎊")
        else:
            st.error(f"Failed: {res.text}")

# ---------------- TRACK PRODUCT BY NAME ---------------- #
elif choice == "Track Product by Name":
    st.subheader("🔍 Track Product by Name")
    product_name = st.text_input("Enter Product Name")
    if st.button("Track", key="track_name"):
        if not product_name.strip():
            st.warning("Please enter a product name.")
        else:
            res = requests.get(f"{API_URL}/track/", params={"name": product_name})
            if res.status_code == 200:
                data = res.json()["Products"]
                for p in data:
                    with st.expander(f"{p['name']}"):
                        st.write(f"PID: {p.get('pid','N/A')}")
                        st.write(f"**Last Price:** {p['lowest_price']} at {p['site']}")
                        st.write(f"URL: {p['url']}")
                        st.write(f"Last Checked: {p['last_checked']}")
                st.success("✨🔍 Product tracking completed! ✨")
            else:
                st.error(f"Failed: {res.text}")

# ---------------- VIEW USERS ---------------- #
elif choice == "View Users":
    st.subheader("👥 View Users")
    res = requests.get(f"{API_URL}/users/")
    if res.status_code == 200:
        users = res.json()
        table_data = []
        for u in users:
            pids = ", ".join(str(p.get("pid")) for p in u.get("products", [])) if u.get("products") else "N/A"
            table_data.append({
                "UID": u.get("uid"),
                "Name": f"{u.get('first_name','')} {u.get('last_name','')}",
                "Email": u.get("email"),
                "Mobile": u.get("mobile_no"),
                "PIDs": pids
            })
        st.table(table_data)
    else:
        st.error(f"Failed: {res.text}")
