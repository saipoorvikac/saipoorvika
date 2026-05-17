import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import speech_recognition as sr

# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI Healthcare Pro UI", layout="wide")

# ================= DATABASE =================
conn = sqlite3.connect("health.db", check_same_thread=False)
c = conn.cursor()
 

c.execute("""
CREATE TABLE IF NOT EXISTS health_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    bp INTEGER,
    sugar INTEGER,
    steps INTEGER,
    calories INTEGER,
    bmi REAL
)
""")
conn.commit()

# ================= LOGIN =================
USER = {"admin":"1234","doctor":"doc123","patient":"pat123"}

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 AI Healthcare Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if USER.get(u)==p:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Invalid login")
    st.stop()

# ================= FUNCTIONS =================
def chatbot(q):
    q = q.lower()
    if "bp" in q:
        return "Reduce salt intake"
    if "diabetes" in q:
        return "Avoid sugar"
    return "Ask health-related question"

def fitness(s):
    if s < 3000:
        return "Low activity"
    if s < 7000:
        return "Moderate"
    return "Excellent"

def diet(s, b):
    if s > 200:
        return "Low sugar diet"
    if b > 30:
        return "Weight loss diet"
    return "Balanced diet"

def medicine(bp, s):
    if bp > 140:
        return "High BP risk"
    if s > 200:
        return "High sugar risk"
    return "Normal"

def voice_input():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as src:
            audio = r.listen(src, timeout=5)
            return r.recognize_google(audio)
    except:
        return "Voice not available"

def report(name, bp, sugar, bmi):
    file = f"{name}_report.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Name: {name}", ln=True)
    pdf.cell(200, 10, f"BP: {bp}", ln=True)
    pdf.cell(200, 10, f"Sugar: {sugar}", ln=True)
    pdf.cell(200, 10, f"BMI: {bmi}", ln=True)
    pdf.output(file)
    return file

# ================= MENU =================
menu = st.sidebar.radio("📌 Navigation", [
    "🏠 Dashboard",
    "➕ Add Patient Data",
    "💬 Chatbot",
    "🥗 Diet Plan",
    "💊 Medicine Check",
    "🏃 Fitness",
    "📄 Report Generator",
    "📊 History",
    "🚨 Emergency",
    "🎤 Voice"
])

# ================= DASHBOARD =================
if menu == "🏠 Dashboard":

    df = pd.read_sql("SELECT * FROM health_metrics", conn)

    st.title("🏥 Healthcare Dashboard")

    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Patients", len(df))
        col2.metric("Avg BP", round(df["bp"].mean(), 2))
        col3.metric("Avg Sugar", round(df["sugar"].mean(), 2))
        col4.metric("Avg BMI", round(df["bmi"].mean(), 2))

        st.plotly_chart(px.line(df, x="name", y="sugar"))
        st.plotly_chart(px.bar(df, x="name", y="bp"))

    st.dataframe(df)

# ================= ADD DATA =================
elif menu == "➕ Add Patient Data":

    name = st.text_input("Name")
    age = st.number_input("Age")
    bp = st.number_input("BP")
    sugar = st.number_input("Sugar")
    steps = st.number_input("Steps")
    calories = st.number_input("Calories")
    bmi = st.number_input("BMI")

    if st.button("Save Patient"):
        c.execute("""
        INSERT INTO health_metrics
        (name,age,bp,sugar,steps,calories,bmi)
        VALUES (?,?,?,?,?,?,?)
        """, (name, age, bp, sugar, steps, calories, bmi))
        conn.commit()
        st.success("Patient saved successfully")

# ================= CHATBOT =================
elif menu == "💬 Chatbot":

    q = st.text_input("Ask Health Question")

    if st.button("Ask"):
        st.info(chatbot(q))

# ================= DIET =================
elif menu == "🥗 Diet Plan":
    s = st.number_input("Sugar")
    b = st.number_input("BMI")

    if st.button("Generate"):
        st.success(diet(s, b))

# ================= MEDICINE =================
elif menu == "💊 Medicine Check":
    bp = st.number_input("BP")
    s = st.number_input("Sugar")

    if st.button("Check"):
        st.warning(medicine(bp, s))

# ================= FITNESS =================
elif menu == "🏃 Fitness":
    s = st.number_input("Steps")

    if st.button("Check"):
        st.success(fitness(s))

# ================= REPORT =================
elif menu == "📄 Report Generator":

    n = st.text_input("Name")
    bp = st.number_input("BP")
    s = st.number_input("Sugar")
    b = st.number_input("BMI")

    if st.button("Generate PDF"):
        file = report(n, bp, s, b)

        with open(file, "rb") as f:
            st.download_button(
                "⬇ Download Report",
                f,
                file_name=file
            )

        st.success("Report generated successfully")

# ================= HISTORY =================
elif menu == "📊 History":

    n = st.text_input("Search Patient")

    if st.button("Search"):
        df = pd.read_sql(
            "SELECT * FROM health_metrics WHERE name LIKE ?",
            conn,
            params=(f"%{n}%",)
        )
        st.dataframe(df)

# ================= EMERGENCY =================
elif menu == "🚨 Emergency":

    df = pd.read_sql("SELECT * FROM health_metrics", conn)

    if df.empty:
        st.warning("No data")
        st.stop()

    st.error("Critical BP Patients")
    st.dataframe(df[df["bp"] > 180])

    st.error("Critical Sugar Patients")
    st.dataframe(df[df["sugar"] > 300])

# ================= VOICE =================
elif menu == "🎤 Voice":

    if st.button("Speak"):
        st.success(voice_input())