import streamlit as st

st.set_page_config(page_title="YouTube Data Warehouse", layout="wide")

st.title("📊 YouTube Data Warehouse")

st.write("""
Welcome to your YouTube Data Warehouse Application!

Use the menu on the left to navigate:
- 📥 **Import Data** (Upload CSV or Run YouTube API Pipeline)
- 📊 **Dashboard** (View Analytics)

Start by selecting a page from the sidebar.
""")

st.sidebar.success("Select a page above 👆")
