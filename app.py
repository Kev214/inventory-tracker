import streamlit as st
import pandas as pd
import db

conn = db.get_connection()
db.init_db(conn)

# This shows as the title on the webpage
st.title("Inventory Tracker")

if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

#adding a search box
term = st.text_input("Search by name")

if term:
    rows = db.search_item(conn,term)
else:
    rows = db.get_all_items(conn)

# Lets get the data and show it 
df = pd.DataFrame([dict(r) for r in rows])
st.dataframe(df)

st.subheader("Low Stock")
cutoff = st.slider("Show items in stock below", 0, 100, 15)

low = db.get_low_stock(conn, cutoff)

#logic for the table to display accurate low_stock data
if low:
    low_df = pd.DataFrame([dict(r) for r in low])
    st.dataframe(low_df)
else:
    st.success("Nothing below the cutoff")

st.subheader("Update Quantity")
update_sku = st.text_input("SKU to update")
new_quantity = st.number_input("New Quantity", min_value = 0)

#logic for updating the quantity 
if st.button("Update"):
    updated = db.update_quantity(conn, update_sku.strip(), int(new_quantity))
    if updated:
        st.session_state["flash"] = f"Updated {update_sku} to {int(new_quantity)}"
        st.rerun()
    else:
        st.error("SKU not found")