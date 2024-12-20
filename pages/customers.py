import streamlit as st
import sqlite3
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

def display():
    st.title("Manage Customers")
    conn = sqlite3.connect("database/quotation.db")
    cursor = conn.cursor()

    # ฟอร์มเพิ่มลูกค้าใหม่
    with st.form("Add Customer"):
        name = st.text_input("Customer Name")
        email = st.text_input("Email")
        address = st.text_area("Address")
        submitted = st.form_submit_button("Add")
        if submitted and name and email:
            cursor.execute("INSERT INTO customers (name, email, address) VALUES (?, ?, ?)", (name, email, address))
            conn.commit()
            st.success("Customer added!")

    # แสดงข้อมูลลูกค้าในตาราง
    st.subheader("Customer List")
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    customers_df = pd.DataFrame(rows, columns=["ID", "Name", "Email", "Address"])

    # การตั้งค่าตาราง AgGrid
    gb = GridOptionsBuilder.from_dataframe(customers_df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_default_column(editable=True)
    gb.configure_selection("single", use_checkbox=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        customers_df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=True,
    )

    # บันทึกการแก้ไข
    edited_df = grid_response["data"]
    if st.button("Save Changes"):
        for index, row in edited_df.iterrows():
            cursor.execute(
                "UPDATE customers SET name = ?, email = ?, address = ? WHERE id = ?",
                (row["Name"], row["Email"], row["Address"], row["ID"]),
            )
        conn.commit()
        st.success("Changes saved!")
        st.experimental_rerun()

    # ลบข้อมูลลูกค้า
    selected_row = grid_response["selected_rows"]
    if selected_row and st.button("Delete Selected Row"):
        selected_id = selected_row[0]["ID"]
        cursor.execute("DELETE FROM customers WHERE id = ?", (selected_id,))
        conn.commit()
        st.success("Customer deleted!")
        st.experimental_rerun()

    conn.close()
