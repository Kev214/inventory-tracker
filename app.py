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