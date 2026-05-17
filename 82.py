import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import speech_recognition as sr
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from fpdf import FPDF

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(page_title="AI Healthcare System", layout="wide")

# =========================================================
# DATABASE
# =========================================================
conn = sqlite3.connect("health.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS health_metrics(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    bp INTEGER,
    sugar INTEGER,
    steps INTEGER,
    calories INTEGER,
    bmi REAL,
    heart_rate INTEGER
)
""")
conn.commit()

# =========================================================
# LOGIN SYSTEM
# =========================================================
USER_CREDENTIALS = {
    "admin": "1234",
    "doctor": "doc123",
    "patient": "pat123"
}

def login(u, p):
    return u in USER_CREDENTIALS and USER_CREDENTIALS[u] == p

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# LOGIN UI
if not st.session_state.logged_in:

    st.title("🔐 Healthcare Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(u, p):
            st.session_state.logged_in = True
            st.success("Login Success")
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.stop()

# =========================================================
# VOICE INPUT
# =========================================================
def voice_input():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎤 Speak now...")
            audio = r.listen(source)
            return r.recognize_google(audio)
    except:
        return "Voice Error"

# =========================================================
# CHATBOT
# =========================================================
def chatbot(q):
    q = q.lower()
    if "fever" in q:
        return "Take rest & drink fluids"
    if "diabetes" in q:
        return "Avoid sugar & exercise daily"
    if "bp" in q:
        return "Reduce salt & stress"
    return "Ask health related questions"

# =========================================================
# DIET
# =========================================================
def diet(sugar, bmi):
    if sugar > 200:
        return "Avoid sugar, eat oats & vegetables"
    if bmi > 30:
        return "Weight loss diet: salads & exercise"
    return "Healthy balanced diet"

# =========================================================
# MEDICINE
# =========================================================
def medicine(bp, sugar):
    if bp > 140:
        return "High BP - consult doctor"
    if sugar > 200:
        return "High sugar - avoid sweets"
    return "Stable condition"

# =========================================================
# FITNESS
# =========================================================
def fitness(steps):
    if steps < 3000:
        return "Walk more"
    if steps < 7000:
        return "Good activity"
    return "Excellent fitness"

# =========================================================
# AYURVEDA
# =========================================================
def ayurveda(bp, sugar):
    if sugar > 200:
        return "Neem, amla juice"
    if bp > 140:
        return "Tulsi tea, yoga"
    return "Meditation, herbal tea"

# =========================================================
# REPORT
# =========================================================
def report(name, bp, sugar, bmi):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Name: {name}", ln=True)
    pdf.cell(200, 10, f"BP: {bp}", ln=True)
    pdf.cell(200, 10, f"Sugar: {sugar}", ln=True)
    pdf.cell(200, 10, f"BMI: {bmi}", ln=True)
    pdf.output("report.pdf")

# =========================================================
# MENU
# =========================================================
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Add Data",
        "Voice",
        "Diet",
        "Medicine",
        "Fitness",
        "Ayurveda",
        "AI Prediction",
        "Report",
        "Goal",
        "Chatbot",
        "History",
        "Appointments",
        "Emergency"
    ]
)

# =========================================================
# ADD DATA
# =========================================================
if menu == "Add Data":

    name = st.text_input("Name")
    age = st.number_input("Age", 1, 120)
    bp = st.number_input("BP")
    sugar = st.number_input("Sugar")
    steps = st.number_input("Steps")
    calories = st.number_input("Calories")
    bmi = st.number_input("BMI")
    heart_rate = st.number_input("Heart Rate")

    if st.button("Save"):

        c.execute("""
        INSERT INTO health_metrics 
        (name, age, bp, sugar, steps, calories, bmi, heart_rate)
        VALUES (?,?,?,?,?,?,?,?)
        """, (name, age, bp, sugar, steps, calories, bmi, heart_rate))

        conn.commit()
        st.success("Saved")

# =========================================================
# DASHBOARD
# =========================================================
elif menu == "Dashboard":

    df = pd.read_sql_query("SELECT * FROM health_metrics", conn)

    st.dataframe(df)

    if not df.empty:
        fig = px.line(df, x="name", y="sugar")
        st.plotly_chart(fig)

# =========================================================
# VOICE
# =========================================================
elif menu == "Voice":

    if st.button("Start Voice"):
        st.success(voice_input())

# =========================================================
# DIET
# =========================================================
elif menu == "Diet":

    s = st.number_input("Sugar")
    b = st.number_input("BMI")

    if st.button("Get Diet"):
        st.success(diet(s, b))

# =========================================================
# MEDICINE
# =========================================================
elif menu == "Medicine":

    bp = st.number_input("BP")
    s = st.number_input("Sugar")

    if st.button("Check"):
        st.info(medicine(bp, s))

# =========================================================
# FITNESS
# =========================================================
elif menu == "Fitness":

    steps = st.number_input("Steps")

    if st.button("Check"):
        st.success(fitness(steps))

# =========================================================
# AYURVEDA
# =========================================================
elif menu == "Ayurveda":

    bp = st.number_input("BP")
    s = st.number_input("Sugar")

    if st.button("Get"):
        st.success(ayurveda(bp, s))

# =========================================================
# AI PREDICTION
# =========================================================
elif menu == "AI Prediction":

    df = pd.read_sql_query("SELECT * FROM health_metrics", conn)

    if len(df) > 5:

        X = df[["bp","sugar","steps","bmi"]]
        y = df["bp"] + df["sugar"]

        model = RandomForestRegressor()
        model.fit(X, y)

        bp = st.number_input("BP")
        s = st.number_input("Sugar")
        steps = st.number_input("Steps")
        bmi = st.number_input("BMI")

        if st.button("Predict"):
            pred = model.predict([[bp,s,steps,bmi]])[0]
            st.success(f"Risk: {pred}")

# =========================================================
# REPORT
# =========================================================
elif menu == "Report":

    name = st.text_input("Name")
    bp = st.number_input("BP")
    s = st.number_input("Sugar")
    bmi = st.number_input("BMI")

    if st.button("Generate"):
        report(name,bp,s,bmi)
        st.success("Report created")

# =========================================================
# GOAL
# =========================================================
elif menu == "Goal":

    g = st.number_input("Goal")
    s = st.number_input("Steps")

    if st.button("Check"):
        if s >= g:
            st.success("Goal achieved")
        else:
            st.warning("Not achieved")

# =========================================================
# CHATBOT
# =========================================================
elif menu == "Chatbot":

    q = st.text_input("Ask health question")

    if st.button("Ask"):
        st.success(chatbot(q))

# =========================================================
# HISTORY
# =========================================================
elif menu == "History":

    name = st.text_input("Search Name")

    if st.button("Search"):
        df = pd.read_sql_query(
            "SELECT * FROM health_metrics WHERE name LIKE ?",
            conn,
            params=(f"%{name}%",)
        )
        st.dataframe(df)

# =========================================================
# APPOINTMENTS
# =========================================================
elif menu == "Appointments":

    n = st.text_input("Name")
    d = st.text_input("Doctor")
    date = st.date_input("Date")

    if st.button("Book"):
        st.success(f"Appointment booked for {n}")

# =========================================================
# EMERGENCY
# =========================================================
elif menu == "Emergency":

    df = pd.read_sql_query("SELECT * FROM health_metrics", conn)

    high_bp = df[df["bp"] > 180]
    high_sugar = df[df["sugar"] > 300]

    st.error("Critical BP Patients")
    st.dataframe(high_bp)

    st.error("Critical Sugar Patients")
    st.dataframe(high_sugar)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption("AI Healthcare System Complete Project")