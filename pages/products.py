import streamlit as st
import sqlite3
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

def display():
    st.title("Manage Products")
    conn = sqlite3.connect("database/quotation.db")
    cursor = conn.cursor()

    # ฟอร์มเพิ่มสินค้าใหม่
    with st.form("Add Product"):
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        unit = st.text_input("Unit")
        submitted = st.form_submit_button("Add")
        if submitted and name and unit:
            cursor.execute("INSERT INTO products (name, price, unit) VALUES (?, ?, ?)", (name, price, unit))
            conn.commit()
            st.success("Product added!")

    # แสดงข้อมูลสินค้าในตาราง
    st.subheader("Product List")
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    products_df = pd.DataFrame(rows, columns=["ID", "Name", "Price", "Unit"])

    # การตั้งค่าตาราง AgGrid
    gb = GridOptionsBuilder.from_dataframe(products_df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_default_column(editable=True)
    gb.configure_selection("single", use_checkbox=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        products_df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=True,
    )

    # บันทึกการแก้ไข
    edited_df = grid_response["data"]
    if st.button("Save Changes"):
        for index, row in edited_df.iterrows():
            cursor.execute(
                "UPDATE products SET name = ?, price = ?, unit = ? WHERE id = ?",
                (row["Name"], row["Price"], row["Unit"], row["ID"]),
            )
        conn.commit()
        st.success("Changes saved!")
        st.experimental_rerun()

    # ลบข้อมูลสินค้า
    selected_row = grid_response["selected_rows"]
    if selected_row and st.button("Delete Selected Row"):
        selected_id = selected_row[0]["ID"]
        cursor.execute("DELETE FROM products WHERE id = ?", (selected_id,))
        conn.commit()
        st.success("Product deleted!")
        st.experimental_rerun()

    conn.close()
