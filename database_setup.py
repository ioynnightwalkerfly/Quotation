import sqlite3

# สร้างการเชื่อมต่อ
conn = sqlite3.connect("database/quotation.db")
cursor = conn.cursor()

# สร้างตารางลูกค้า
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT
)
""")

# สร้างตารางสินค้า
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    unit TEXT NOT NULL
)
""")

# สร้างตารางใบเสนอราคา
cursor.execute("""
CREATE TABLE IF NOT EXISTS quotations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    products TEXT NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
)
""")

# บันทึกและปิดการเชื่อมต่อ
conn.commit()
conn.close()
print("Database setup complete.")
