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

def update_quantity(conn, sku, new_quantity):
    curr = conn.execute(
        "UPDATE items SET quantity = ? WHERE sku = ?",
        (new_quantity,sku)
    )
    conn.commit()
    return curr.rowcount > 0

def update_price(conn, sku, new_price):
    curr = conn.execute(
        "UPDATE items SET price = ? WHERE sku = ?",
        (new_price,sku)
    )
    conn.commit()
    return curr.rowcount > 0

def search_item(conn, term):
    pattern = f"%{term}%"
    curr = conn.execute(
        "SELECT name "
        "FROM items "
        "WHERE name LIKE ? "
        "ORDER BY name",
        (pattern,),
    )
    return curr.fetchall()

def get_low_stock(conn, cutoff):
    curr = conn.execute(
        "SELECT * "
        "FROM items "
        "WHERE quantity < ? "
        "ORDER BY quantity ASC",
        (cutoff,),
    )
    return curr.fetchall()

def get_all_items(conn):
    curr = conn.execute("SELECT * FROM items ORDER BY sku")
    return curr.fetchall()

