import csv

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