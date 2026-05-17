import streamlit as st
import sqlite3
import pandas as pd

# ---------- LOGIN DATA ----------
USER_CREDENTIALS = {
    "admin": "1234",
    "sumanth": "pass123",
    "saipoorvika":"sai@123",
    "varsha":"var@321",
    "bindu":"bin@321"
}

# ---------- LOGIN FUNCTION ----------
def login(username, password):
    return username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password


# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------- LOGIN PAGE ----------
if not st.session_state.logged_in:
    st.title(" Login Page")

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.success("Login successful ")
            st.rerun()
        else:
            st.error("Invalid username or password ")

# ---------- MAIN APP (YOUR ORIGINAL CODE) ----------
else:

    def init_db():
        conn = sqlite3.connect("health.db")
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS health_metrics (
            name TEXT,
            bp INTEGER,
            sugar INTEGER
        )
        """)
        conn.commit()
        conn.close()

    init_db()

    # Insert data
    def insert_data(name, bp, sugar):
        conn = sqlite3.connect("health.db")
        c = conn.cursor()
        c.execute("INSERT INTO health_metrics VALUES (?, ?, ?)", (name, bp, sugar))
        conn.commit()
        conn.close()

    # Fetch data
    def get_data():
        conn = sqlite3.connect("health.db")
        df = pd.read_sql_query("SELECT * FROM health_metrics", conn)
        conn.close()
        return df

    # ---------- UI ----------
    st.title(" Healthcare Assistant")

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    name = st.text_input("Enter Name")
    bp = st.number_input("Blood Pressure", 0, 300)
    sugar = st.number_input("Sugar Level", 0, 500)

    if st.button("Save Data"):
        insert_data(name, bp, sugar)
        st.success("Data saved successfully!")

    # Show table
    st.subheader("Stored Data")
    st.dataframe(get_data())