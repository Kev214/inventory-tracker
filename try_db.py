import db

conn = db.get_connection(":memory")
print(conn)

