# Zewail Library

A desktop library / bookstore app built with Python and Tkinter, my first-year university project.

## Features

**Guest mode**
- Browse the book library
- Store with category filter and buy list
- Checkout with promo codes, tax and a receipt
- Rate books (1-5)
- Report a problem

**Admin mode** (password protected)
- View and edit books, add new books
- Create promo codes
- View profits from orders
- Read user reports
- Change the admin password

Data is stored in plain CSV files (`library.csv`, `orders.csv`, `buylist.csv`, `promos.csv`, `reports.csv`).

## Run it

Requires Python 3 with Tkinter (included in most Python installs).

```
python main_app.py
```

The default admin password is `admin123`. Change it from the Admin mode "Change Password" tab. The password is stored as a SHA-256 hash in `admin_password.txt`, which is created on first run and is gitignored.

## Files

- `main_app.py` - entry point, admin/guest selection window
- `guest_gui.py` - guest interface
- `admin_gui.py` - admin interface
- `passwords_and_checking.py` - admin login and password handling
- `*.csv` - data files (books, orders, promo codes, reports)
