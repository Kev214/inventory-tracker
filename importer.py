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
