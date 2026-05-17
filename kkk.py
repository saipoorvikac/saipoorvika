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
    st.title("🔐 Login Page")

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    
    if st.button("Login", key="login_main"):
        if login(username, password):
            st.session_state.logged_in = True
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid username or password ❌")

    st.stop()

# ---------- DATABASE ----------
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

    c.execute("""
    CREATE TABLE IF NOT EXISTS health(
        name TEXT,
        steps INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- INSERT ----------
def insert_data(name, bp, sugar, steps):
    conn = sqlite3.connect("health.db")
    c = conn.cursor()

    c.execute("INSERT INTO health_metrics VALUES (?, ?, ?)", (name, bp, sugar))
    c.execute("INSERT INTO health VALUES (?, ?)", (name, steps))

    conn.commit()
    conn.close()

# ---------- FETCH ----------
def get_data():
    conn = sqlite3.connect("health.db")
    df = pd.read_sql_query("SELECT * FROM health_metrics", conn)
    conn.close()
    return df

# ---------- MAIN UI ----------
st.title("🏥 Healthcare App")

menu = ["Add Data", "View Data", "Fitness", "Medicine", "Report"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------- ADD DATA ----------
if choice == "Add Data":
    st.subheader("Add Health Data")

    name = st.text_input("Name")
    bp = st.number_input("Blood Pressure")
    sugar = st.number_input("Sugar")
    steps = st.number_input("Steps")

    if st.button("Save", key="save_btn"):
        insert_data(name, bp, sugar, steps)
        st.success("Data Saved")

# ---------- VIEW DATA ----------
elif choice == "View Data":
    st.subheader("View Records")

    df = get_data()

    if not df.empty:
        st.dataframe(df)
        st.line_chart(df[['bp', 'sugar']])
    else:
        st.warning("No data found")

    conn = sqlite3.connect("health.db")
    df2 = pd.read_sql_query("SELECT * FROM health", conn)
    st.subheader("Steps Data")
    st.dataframe(df2)
    conn.close()

# ---------- FITNESS ----------
elif choice == "Fitness":
    st.subheader("Fitness Tracker")

    weight = st.number_input("Weight (kg)")
    height = st.number_input("Height (m)")
    minutes = st.number_input("Exercise Minutes")

    if st.button("Calculate", key="fit_btn"):
        if height == 0:
            st.error("Height cannot be 0")
        else:
            bmi = weight / (height ** 2)
            calories = minutes * 5

            st.success(f"BMI: {round(bmi,2)}")
            st.success(f"Calories Burned: {calories}")

# ---------- MEDICINE ----------
elif choice == "Medicine":
    st.subheader("Medicine Checker")

    med1 = st.text_input("Medicine 1")
    med2 = st.text_input("Medicine 2")

    if st.button("Check", key="med_btn"):
        if med1 == "Paracetamol" and med2 == "Ibuprofen":
            st.success("✅ Safe")
        else:
            st.warning("⚠ Consult Doctor")

# ---------- REPORT ----------
elif choice == "Report":
    st.subheader("Health Report")

    name = st.text_input("Name")
    bp = st.number_input("BP")
    sugar = st.number_input("Sugar")

    if st.button("Generate", key="rep_btn"):
        bp_status = "High BP" if bp > 140 else "Normal BP"
        sugar_status = "High Sugar" if sugar > 180 else "Normal Sugar"

        st.success(f"{name}: {bp_status}, {sugar_status}")

    # ---------- Goal tracking ----------
    st.subheader("Goal Tracking")
    goal = st.number_input("Set Step Goal")
    steps = st.number_input("Enter Current Steps")

    df = get_data()

    if not df.empty:
        st.line_chart(df[['bp', 'sugar']])
    else:
        st.warning("No data to display")

    if goal > 0:
        if steps >= goal:
            st.success("🎯 Goal Achieved")
        else:
            st.warning("Keep trying")