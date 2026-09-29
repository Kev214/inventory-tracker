import sqlite3

DB_PATH = "inventory.db"

def get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items(
            sku TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()

def add_item(conn, sku, name, category, price, quantity):
    conn.execute(
        "INSERT INTO items (sku, name, category, price, quantity) "
        "VALUES (?,?,?,?,?)",
        (sku, name, category, price, quantity),
    )
    conn.commit()

#finds every column from the row whose sku matches
#and fetchone() returns the first matching row or NONE if it does not exist
def get_item(conn, sku):
    curr = conn.execute(
        "SELECT * FROM items WHERE sku =?",
        (sku,), 
    )
    return curr.fetchone()