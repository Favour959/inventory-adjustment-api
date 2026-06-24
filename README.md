# Inventory Adjustment API

A REST API built with **Django** and **Django REST Framework** that tracks product stock changes with a full audit trail.

## What it does

| Endpoint | Method | Description |
|---|---|---|
| `/inventory/adjust` | POST | Increase or decrease a product's stock |
| `/inventory/history` | GET | View all adjustments ever made |

**Rules enforced:**
- Stock can never go negative
- Every adjustment must have a reason
- Every adjustment is permanently recorded

---

## Setup (do this once)

**Requirements:** Python must be installed on your computer.
Check with: `python --version`

```bash
# 1. Clone the project
git clone https://github.com/oguadinma-favour/inventory-adjustment-api.git
cd inventory-adjustment-api

# 2. Create and activate a virtual environment
python -m venv inventory_env

# Windows:
inventory_env\Scripts\activate
# Mac/Linux:
source inventory_env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up the database
python manage.py migrate

# 5. Create an admin account
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

Server runs at: **http://127.0.0.1:8000**

> Every time you return to this project in a new terminal, activate the virtual environment first (step 2) before running any commands.

---

## Create a test product first

1. Go to **http://127.0.0.1:8000/admin/**
2. Log in with the account you created in step 5
3. Click **Products → Add Product**
4. Set any name and a starting stock (e.g. `Blue Widget`, stock `50`)
5. Click **Save** — the product will have **id: 1**

---

## Testing the API

### Option A — Browser (no extra tools needed)

- **History:** visit `http://127.0.0.1:8000/inventory/history` directly in your browser
- **Adjust:** visit `http://127.0.0.1:8000/inventory/adjust`, scroll to the bottom, paste JSON into the Content box and click POST

### Option B — Postman

Download free at: https://www.postman.com/downloads/

**Increase stock:**
```json
POST http://127.0.0.1:8000/inventory/adjust

{
    "product_id": 1,
    "adjustment": 10,
    "reason": "New stock received"
}
```

**Decrease stock:**
```json
POST http://127.0.0.1:8000/inventory/adjust

{
    "product_id": 1,
    "adjustment": -5,
    "reason": "Sold to customer"
}
```

**View all history:**
GET  http://127.0.0.1:8000/inventory/history

---

## Run the automated tests

Open a second terminal, activate the virtual environment, then:

```bash
python manage.py test inventory -v 2
```

Expected: `Ran 10 tests — OK`

---

## Common errors

| Error | Fix |
|---|---|
| `No module named django` | Virtual environment is not active — run the activate command again |
| `No installed app with label inventory` | Check that `'inventory'` is in `INSTALLED_APPS` inside `inventory_project/settings.py` |
| `Port 8000 already in use` | Run `python manage.py runserver 8001` instead |
| `404 at /` | Correct — there is no homepage. Use the endpoints above |

---

## Built with

- Python 
- Django 
- Django REST Framework 