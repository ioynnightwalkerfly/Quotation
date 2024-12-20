import streamlit as st
import sqlite3
import pandas as pd

def display():
    st.title("Create Quotation")
    conn = sqlite3.connect("database/quotation.db")
    cursor = conn.cursor()

    # เลือกลูกค้า
    cursor.execute("SELECT id, name FROM customers")
    customers = cursor.fetchall()
    customer_dict = {name: customer_id for customer_id, name in customers}
    selected_customer = st.selectbox("Select Customer", options=list(customer_dict.keys()))
    
    # เลือกสินค้า
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    products_df = pd.DataFrame(products, columns=["ID", "Name", "Price", "Unit"])
    st.dataframe(products_df)

    selected_products = st.multiselect("Select Products", options=products_df["Name"])
    selected_df = products_df[products_df["Name"].isin(selected_products)]

    # คำนวณรวมราคา
    if not selected_df.empty:
        total = selected_df["Price"].sum()
        st.write(f"**Total: {total}**")

        # บันทึกใบเสนอราคา
        if st.button("Save Quotation"):
            product_list = ", ".join(selected_products)
            cursor.execute(
                "INSERT INTO quotations (customer_id, products, total) VALUES (?, ?, ?)",
                (customer_dict[selected_customer], product_list, total),
            )
            conn.commit()
            st.success("Quotation saved!")

    # แสดงใบเสนอราคาที่บันทึก
    st.subheader("Saved Quotations")
    cursor.execute("""
    SELECT q.id, c.name, q.products, q.total
    FROM quotations q
    JOIN customers c ON q.customer_id = c.id
    """)
    quotations = cursor.fetchall()
    quotations_df = pd.DataFrame(quotations, columns=["ID", "Customer", "Products", "Total"])
    st.dataframe(quotations_df)

    conn.close()
