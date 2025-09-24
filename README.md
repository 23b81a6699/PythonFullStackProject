# E-commerce Product Price Tracker

## Overview
E-commerce Product Price Tracker is an application that tracks product prices of leading e-commerce sites such as Amazon and Flipkart. It allows users to register, add products by entering their URLs, and set a target price. The application scrapes the product pages at regular time intervals automatically, stores price history in a history table, and updates the current price in the database. If a price reduction is identified below the desired price of the user, the system is capable of informing the user (via email or dashboard alert). This enables users to save money when purchasing products at the optimal price and offers a full price history for review.


## Features
- User registration and management
- Add products to track using URLs
- Set target (desired) price for each product
- Automatic price scraping at configurable intervals
- Maintains price history for analysis
- Alerts users when prices drop below the target


## Project Stucture

E-commerce Product Price Tracker/
|
|----src/                # core application logic
|      |---logic.py    # Business logic and task operations
|      |__db.py       # Database operations
|
|----API/                # Backend API
|      |__main.py    # FastAPI endpoints
|
|----frontend/        # Frontend application
|     |__app.py      # Streamlit web interface
|
|----requirements.txt    # python dependies
|----README.md        # project Documentation
|
|----.env

## Quick Start

## Prerequistes

Python 3.8 or higher
A supabase account
Git(Push , cloning)

### 1. Clone or Download the Project

# Option 1: Clone with Git
git clone <repository-url>

# Option 2: Download and extract the ZIP file

### 2. Install Dependies

# Install all required Python packages
pip install -r requirements.txt

### 3. Set up Supabase Database

1. Create a Supabase Project :
2. Create the users table :

-Go to the SQL Editor in your Supabase dashbord
-Run this SQL Command :

``` sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT,
    email TEXT UNIQUE NOT NULL,
    mobile_no TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    name TEXT,
    category TEXT,
    last_price REAL,
    desired_price REAL,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```
#  **Get your Credentials :
### 4. Configure Environment Variables  

1. Create a `.env` file in the project root

2. Add your supabase credentials to `.env`:

SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_key_here

**Example:**
SUPABASE_URL="https://swelytillpyabxhjclse.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN3ZWx5dGlsbHB5YWJ4aGpjbHNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODIyMzIsImV4cCI6MjA3MzY1ODIzMn0.IczsYYyr4J-60OYrfEeiuORqEqT4tHts17J-K6y94Qo"

## 5. Run the Application

# Streamlit Frontend

streamlit run Frontend/app.py

This app will open in your browser at `http://localhost:8501`

## FastAPI Backend

cd API
python main.py

the API will be available at `http://localhost:8000`

## How to Use
1.  Run the Streamlit app: `streamlit run frontend/app.py`.
2.  Register, then log in.
3.  On your dashboard, enter a product URL and desired price to start tracking.

## Technical Details
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Scraping**: `requests` & `BeautifulSoup`

## Technologies Used

**Frontend** : Streamlit (python web framework)
**Backend** : FastAPI ( python REST API framework)
**Database** : Supabase (PostgreSQL - based backend-as-a-service)
**Language** : Python 3.8+

## Key Components

1. **`src/db.py`**: Handles all database connections and data operations with Supabase.

2. **`src/logic.py`**: Contains the core logic for web scraping, password handling, and user management.

3. **`API/main.py`**: Defines the backend API endpoints that the frontend calls.

4. **`Frontend/app.py`**: Creates the user-facing web application interface using Streamlit.

### Common Errors

1. **`ModuleNotFoundError`**:
   - Make sure you've installed all dependies: `pip install -r requirements.txt`
   - Check that you're running commands from the correct directory

## Future Enhancements

Ideas for extending this project:

1. Add price drop notifications via SMS, WhatsApp, or app alerts.

2. Enable price history charts for interactive trend analysis.

3. Support tracking across multiple e-commerce platforms, not just Amazon and Flipkart.

4. Implement AI-based prediction for future price trends.

5. Provide automatic order tracking and purchase analytics tools.

Integrate user-customizable alert thresholds and notification schedules.
## Technology Stack
- **Programming Language:** Python  
- **Web Scraping:** Requests + BeautifulSoup (or Playwright for JS-rendered pages)  
- **Database:** SQLite (or PostgreSQL/MySQL for production)  
- **Scheduling:** `schedule` or `APScheduler`  
- **Environment Management:** `python-dotenv` for sensitive credentials  
- **Notifications:** Email or dashboard alerts  

---


