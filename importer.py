import csv
import db

#Removes trailing and leading empty spaces
def clean_text(s):
    return s.strip()

#Capitalizes each word and then other lettes are lowercast
def clean_name(s):
    return " ".join(word.capitalize() for word in s.strip().split())

#changes any dollar sign to normal float
def clean_price(s):
    s = s.strip().replace("$", "")
    if s == "":
        raise ValueError("blank price")
    return float(s)

#prevents negative quantity
def clean_quantity(s):
    s = s.strip()
    if s == "":
        return 0
    q = int(s)
    if q < 0:
        raise ValueError("Negative quantity")
    return q

#this function cleans an entire row 
def clean_row(row):
    sku = clean_text(row["sku"])
    if sku == "":
        raise ValueError("Empty SKU")

    return {
        "sku" : sku,
        "name": clean_name(row["name"]),
        "category": clean_name(row["category"]),
        "price": clean_price(row["price"]),
        "quantity": clean_quantity(row["quantity"])
    }

def read_clean_rows(path):
    clean = {}
    rejected = []
    duplicates = 0

    with open(path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cleaned = clean_row(row)
            except ValueError as e:
                rejected.append((row,str(e)))
                continue

            if cleaned["sku"] in clean:
                duplicates += 1

            clean[cleaned["sku"]] = cleaned

    return clean, rejected, duplicates

def load_items(conn, items):
    inserted = 0
    failed = []

    for item in items.values():
        try:
            db.add_item(conn, item["sku"], item["name"], item["category"], item["price"], item["quantity"])
            inserted += 1
        except ValueError as e:
            failed.append((item["sku"], str(e)))

    return inserted, failed

def main():
    conn = db.get_connection()
    db.init_db(conn)

    #clean up the db so we can actually check for inserts
    conn.execute("DELETE FROM items")
    conn.commit()

    clean, rejected, duplicates = read_clean_rows("data/messy_inventory.csv")
    inserted, failed = load_items(conn,clean)

    print("Rows read: ", len(clean) + len(rejected) + duplicates)
    print("Rejected: ", len(rejected))
    for row, reason in rejected:
        print(" ", row["sku"] or "(blank)", "->", reason)
    print("Duplicated: ", duplicates)
    print("Inserted: ", inserted)
    if failed:
        print("Failed inserts: ", failed)

if __name__ == "__main__":
    main()
    