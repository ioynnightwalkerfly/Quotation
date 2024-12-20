import streamlit as st

st.set_page_config(page_title="Quotation App", layout="wide")

st.sidebar.title("Menu")
menu = st.sidebar.radio("Go to", ["Manage Customers", "Manage Products", "Create Quotation"])

if menu == "Manage Customers":
    from pages import customers
    customers.display()
elif menu == "Manage Products":
    from pages import products
    products.display()
elif menu == "Create Quotation":
    from pages import create_quote
    create_quote.display()
