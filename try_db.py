import db

conn = db.get_connection(":memory:")
print(conn)

db.init_db(conn)
print("init_db ok")

db.add_item(conn, "9001", "Test Milk", "dairy", 5.49, 10)
print("ADDED")

row = db.get_item(conn,"9001")
print(row["name"], row["price"])

rows = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
names = []
for r in rows:
    names.append(r["name"])
print(names)



