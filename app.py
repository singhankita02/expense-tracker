import streamlit as st
import uuid
from decimal import Decimal
from datetime import datetime
import pandas as pd
from db import init_db, get_connection

init_db()
st.title("💰 Expense Tracker")

conn = get_connection()

st.subheader("Add Expense")

amount = st.text_input("Amount")
category = st.text_input("Category")
description = st.text_input("Description")
date = st.date_input("Date")

if st.button("Add Expense"):
    try:
        amt = Decimal(amount)
        if amt <= 0:
            st.error("Amount must be positive")
        else:
            client_request_id = str(uuid.uuid4())
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO expenses
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                client_request_id,
                str(amt),
                category,
                description,
                date.isoformat(),
                datetime.utcnow().isoformat()
            ))
            conn.commit()
            st.success("Expense added safely")
    except:
        st.error("Invalid input")

st.subheader("Expenses")

filter_category = st.text_input("Filter by category")
query = "SELECT * FROM expenses"
params = []

if filter_category:
    query += " WHERE category = ?"
    params.append(filter_category)

query += " ORDER BY date DESC"

df = pd.read_sql_query(query, conn, params=params)

if not df.empty:
    df["amount"] = df["amount"].astype(float)
    st.table(df)
    st.success(f"Total: ₹{df['amount'].sum()}")
else:
    st.info("No expenses found")
