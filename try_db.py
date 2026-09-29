import db

conn = db.get_connection(":memory")
print(conn)

db.init_db(conn)
db.init_db(conn)
print("init_db ok")

rows = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
names = []
for r in rows:
    names.append(r["name"])
print(names)

