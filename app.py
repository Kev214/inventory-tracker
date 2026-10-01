import streamlit as st
import pandas as pd
import db

conn = db.get_connection()
db.init_db(conn)

# This shows as the title on the webpage
st.title("Inventory Tracker")

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

if low:
    low_df = pd.DataFrame([dict(r) for r in low])
    st.dataframe(low_df)
else:
    st.success("Nothing below the cutoff")