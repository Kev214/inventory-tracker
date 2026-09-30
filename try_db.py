import db

conn = db.get_connection(":memory:")
print(conn)

db.init_db(conn)
print("init_db ok")

#tests to see if the new item is added correctly
db.add_item(conn, "9001", "Test Milk", "dairy", 5.49, 10)
print("ADDED")

#tests if the item with the given sku number is printed
row = db.get_item(conn,"9001")
print(row["name"], row["price"])

#prints the tables that have been created 
rows = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
names = []
for r in rows:
    names.append(r["name"])
print(names)

#testing to see if the update_quantity function works
print(db.update_quantity(conn,"9001", 90))
print(db.get_item(conn,"9001")["quantity"])

#testing to see if the update_price function works
print(db.update_price(conn,"9001", 6.00))
print(db.get_item(conn,"9001")["price"])


