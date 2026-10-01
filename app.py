import streamlit as st
import pandas as pd
import db

conn = db.get_connection()
db.init_db(conn)

# This shows as the title on the webpage
st.title("Inventory Tracker")

# Lets get the data and show it 
rows = db.get_all_items(conn)
df = pd.DataFrame([dict(r) for r in rows])
st.dataframe(df)