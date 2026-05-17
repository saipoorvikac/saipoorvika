import streamlit as st
import sqlite3
import pandas as pd

DB_NAME = "health.db"


# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Health metrics
    c.execute("""
    CREATE TABLE IF NOT EXISTS health_metrics (
        name TEXT,
        bp INTEGER,
        sugar INTEGER,
        steps INTEGER,
        calories INTEGER
    )
    """)

    # Medication database (Indian meds)
    c.execute("""
    CREATE TABLE IF NOT EXISTS medications (
        name TEXT,
        salt TEXT,
        uses TEXT,
        source TEXT
    )
    """)

    # Ayurveda knowledge base
    c.execute("""
    CREATE TABLE IF NOT EXISTS ayurveda (
        condition TEXT,
        recommendation TEXT
    )
    """)

    # Diet table (regional India)
    c.execute("""
    CREATE TABLE IF NOT EXISTS diet (
        region TEXT,
        food TEXT
    )
    """)

    # Insurance + medical history
    c.execute("""
    CREATE TABLE IF NOT EXISTS insurance (
        name TEXT,
        provider TEXT,
        policy_number TEXT,
        history TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- INSERT HEALTH DATA ----------------
def insert_health(name, bp, sugar, steps, calories):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO health_metrics VALUES (?, ?, ?, ?, ?)
    """, (name, bp, sugar, steps, calories))

    conn.commit()
    conn.close()


# ---------------- FETCH ----------------
def get_health():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM health_metrics", conn)
    conn.close()
    return df


# ---------------- SIMPLE API MOCKS ----------------
def onemg_search(medicine):
    # placeholder for Tata 1mg API
    return {
        "medicine": medicine,
        "source": "1mg (mock)",
        "status": "available"
    }


def practo_doctors(city, speciality):
    # placeholder for Practo API
    return pd.DataFrame([
        {"name": "Dr. Kumar", "city": city, "speciality": speciality, "rating": 4.6},
        {"name": "Dr. Sharma", "city": city, "speciality": speciality, "rating": 4.4}
    ])


def ayurveda_reco(condition):
    data = {
        "fever": "Tulsi + Ginger + warm water",
        "diabetes": "Fenugreek + Bitter gourd",
        "bp": "Garlic + meditation + low salt diet"
    }
    return data.get(condition.lower(), "Consult Ayurveda expert")


def diet_recommendation(region):
    diets = {
        "north": ["roti", "dal", "rice"],
        "south": ["idli", "dosa", "sambar"],
        "west": ["bhakri", "vegetables"],
        "east": ["rice", "fish curry"]
    }
    return diets.get(region.lower(), ["balanced diet"])


# ---------------- UI ----------------
st.title("🏥 Indian AI Health Platform")

menu = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Health Tracker",
        "Medicine Search (1mg)",
        "Doctors (Practo)",
        "Ayurveda",
        "Diet Plan",
        "Insurance"
    ]
)


# ================= HEALTH TRACKER =================
if menu == "Health Tracker":
    st.header("📊 Health Tracker")

    name = st.text_input("Name")
    bp = st.number_input("BP", 0, 300)
    sugar = st.number_input("Sugar", 0, 500)
    steps = st.number_input("Steps", 0, 100000)
    calories = st.number_input("Calories", 0, 10000)

    if st.button("Save"):
        insert_health(name, bp, sugar, steps, calories)
        st.success("Saved!")

    df = get_health()
    st.dataframe(df)

    if not df.empty:
        st.line_chart(df[["steps", "calories"]])


# ================= MEDICINE (1MG MOCK) =================
elif menu == "Medicine Search (1mg)":
    st.header("💊 Medicine Search (1mg)")

    med = st.text_input("Enter medicine name")

    if st.button("Search"):
        result = onemg_search(med)
        st.json(result)


# ================= PRACTO DOCTORS =================
elif menu == "Doctors (Practo)":
    st.header("👨‍⚕️ Find Doctors")

    city = st.text_input("City")
    spec = st.text_input("Speciality")

    if st.button("Search Doctors"):
        df = practo_doctors(city, spec)
        st.dataframe(df)


# ================= AYURVEDA =================
elif menu == "Ayurveda":
    st.header("🌿 Ayurveda Recommendations")

    condition = st.text_input("Enter condition (fever/bp/diabetes)")

    if st.button("Get Advice"):
        st.success(ayurveda_reco(condition))


# ================= DIET =================
elif menu == "Diet Plan":
    st.header("🍛 Indian Diet Plan")

    region = st.selectbox("Select Region", ["north", "south", "east", "west"])

    st.write("Recommended foods:")
    st.write(diet_recommendation(region))


# ================= INSURANCE =================
elif menu == "Insurance":
    st.header("🏥 Medical Insurance & History")

    name = st.text_input("Name")
    provider = st.text_input("Insurance Provider")
    policy = st.text_input("Policy Number")
    history = st.text_area("Medical History")

    if st.button("Save Insurance"):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO insurance VALUES (?, ?, ?, ?)",
                  (name, provider, policy, history))
        conn.commit()
        conn.close()
        st.success("Saved Insurance Data")












# app.py
# Run using: streamlit run app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import re
from datetime import datetime
from fpdf import FPDF

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Health Monitoring System",
    page_icon="🩺",
    layout="wide"
)

# ==========================================
# DATABASE
# ==========================================
DB_NAME = "health_monitor.db"


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS health_metrics(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        weight REAL,
        blood_pressure TEXT,
        sugar REAL,
        heart_rate INTEGER,
        sleep REAL,
        steps INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS medications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine TEXT,
        dosage TEXT,
        frequency TEXT,
        reminder TEXT,
        adherence INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS goals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_name TEXT,
        target REAL,
        current REAL,
        target_date TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


create_tables()

# ==========================================
# VALIDATION
# ==========================================


def validate_bp(bp):
    pattern = r"^\d{2,3}/\d{2,3}$"
    return re.match(pattern, bp)


def validate_weight(weight):
    return 20 <= weight <= 300


def validate_hr(hr):
    return 30 <= hr <= 220


# ==========================================
# DATABASE FUNCTIONS
# ==========================================


def add_health_data(date, weight, bp, sugar, hr, sleep, steps):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO health_metrics
    (date, weight, blood_pressure, sugar, heart_rate, sleep, steps)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (date, weight, bp, sugar, hr, sleep, steps))

    conn.commit()
    conn.close()


def get_health_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM health_metrics", conn)
    conn.close()
    return df


def add_medication(medicine, dosage, frequency, reminder, adherence):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO medications
    (medicine, dosage, frequency, reminder, adherence)
    VALUES (?, ?, ?, ?, ?)
    """, (medicine, dosage, frequency, reminder, adherence))

    conn.commit()
    conn.close()


def get_medications():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM medications", conn)
    conn.close()
    return df


def add_goal(goal_name, target, current, target_date, status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO goals
    (goal_name, target, current, target_date, status)
    VALUES (?, ?, ?, ?, ?)
    """, (goal_name, target, current, target_date, status))

    conn.commit()
    conn.close()


def get_goals():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM goals", conn)
    conn.close()
    return df


# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.title("🏥 Health App")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Health Entry",
        "Medication Tracker",
        "Health Goals",
        "Medical Lookup",
        "Export Reports"
    ]
)

# ==========================================
# DASHBOARD
# ==========================================
if menu == "Dashboard":

    st.title("📊 Health Dashboard")

    df = get_health_data()

    if df.empty:
        st.warning("No health data available")
    else:
        latest = df.iloc[-1]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Weight", f"{latest['weight']} kg")
        col2.metric("Heart Rate", f"{latest['heart_rate']} bpm")
        col3.metric("Sugar", f"{latest['sugar']} mg/dL")
        col4.metric("Steps", latest['steps'])

        st.subheader("📈 Weight Trend")

        fig = px.line(
            df,
            x="date",
            y="weight",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("❤️ Heart Rate Trend")

        fig2 = px.bar(
            df,
            x="date",
            y="heart_rate",
            color="heart_rate"
        )

        st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# HEALTH ENTRY
# ==========================================
elif menu == "Health Entry":

    st.title("📝 Add Health Data")

    with st.form("health_form"):

        date = st.date_input("Date")

        weight = st.number_input(
            "Weight (kg)",
            min_value=0.0
        )

        bp = st.text_input(
            "Blood Pressure (Example: 120/80)"
        )

        sugar = st.number_input(
            "Blood Sugar"
        )

        hr = st.number_input(
            "Heart Rate"
        )

        sleep = st.number_input(
            "Sleep Hours"
        )

        steps = st.number_input(
            "Steps"
        )

        submit = st.form_submit_button("Save")

        if submit:

            try:

                if not validate_weight(weight):
                    st.error("Invalid weight")

                elif not validate_bp(bp):
                    st.error("Invalid BP format")

                elif not validate_hr(hr):
                    st.error("Invalid heart rate")

                else:

                    add_health_data(
                        str(date),
                        weight,
                        bp,
                        sugar,
                        hr,
                        sleep,
                        steps
                    )

                    st.success("Health data saved")

            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================
# MEDICATION TRACKER
# ==========================================
elif menu == "Medication Tracker":

    st.title("💊 Medication Tracker")

    with st.form("med_form"):

        medicine = st.text_input("Medicine Name")

        dosage = st.text_input("Dosage")

        frequency = st.selectbox(
            "Frequency",
            [
                "Once Daily",
                "Twice Daily",
                "Weekly"
            ]
        )

        reminder = st.time_input("Reminder Time")

        adherence = st.slider(
            "Adherence %",
            0,
            100,
            80
        )

        med_submit = st.form_submit_button("Add Medication")

        if med_submit:

            try:

                if len(medicine.strip()) < 2:
                    st.error("Medicine name too short")

                else:

                    add_medication(
                        medicine,
                        dosage,
                        frequency,
                        str(reminder),
                        adherence
                    )

                    st.success("Medication added")

            except Exception as e:
                st.error(f"Error: {e}")

    meds = get_medications()

    if not meds.empty:

        st.subheader("📋 Medication Records")

        st.dataframe(meds)

        st.subheader("📊 Adherence Report")

        fig = px.pie(
            meds,
            names="medicine",
            values="adherence"
        )

        st.plotly_chart(fig)

# ==========================================
# GOALS
# ==========================================
elif menu == "Health Goals":

    st.title("🎯 Health Goals")

    with st.form("goal_form"):

        goal_name = st.text_input("Goal Name")

        target = st.number_input("Target Value")

        current = st.number_input("Current Value")

        target_date = st.date_input("Target Date")

        submit_goal = st.form_submit_button("Save Goal")

        if submit_goal:

            try:

                progress = 0

                if target > 0:
                    progress = int((current / target) * 100)

                status = "Completed" if progress >= 100 else "In Progress"

                add_goal(
                    goal_name,
                    target,
                    current,
                    str(target_date),
                    status
                )

                st.success("Goal saved")

            except Exception as e:
                st.error(f"Error: {e}")

    goals = get_goals()

    if not goals.empty:

        for _, row in goals.iterrows():

            st.subheader(row["goal_name"])

            progress = int(
                (row["current"] / row["target"]) * 100
            )

            st.progress(min(progress, 100))

            st.write("Status:", row["status"])

            st.write("Target Date:", row["target_date"])

# ==========================================
# MEDICAL LOOKUP
# ==========================================
elif menu == "Medical Lookup":

    st.title("🔎 Medical Information Lookup")

    query = st.text_input(
        "Enter disease or medicine"
    )

    if st.button("Search"):

        medical_data = {
            "Diabetes": {
                "info": "Diabetes affects blood sugar regulation.",
                "source": "https://www.who.int/health-topics/diabetes"
            },
            "Hypertension": {
                "info": "Hypertension is high blood pressure.",
                "source": "https://www.cdc.gov/bloodpressure/"
            }
        }

        found = False

        for key in medical_data:

            if query.lower() in key.lower():

                found = True

                st.subheader(key)

                st.write(
                    medical_data[key]["info"]
                )

                st.write(
                    "Source:",
                    medical_data[key]["source"]
                )

        if not found:
            st.warning("No information found")

# ==========================================
# EXPORT REPORTS
# ==========================================
elif menu == "Export Reports":

    st.title("📤 Export Reports")

    health_df = get_health_data()

    if st.button("Generate CSV"):

        try:

            health_df.to_csv(
                "health_report.csv",
                index=False
            )

            st.success("CSV Generated")

            with open(
                "health_report.csv",
                "rb"
            ) as file:

                st.download_button(
                    label="Download CSV",
                    data=file,
                    file_name="health_report.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("Generate PDF"):

        try:

            pdf = FPDF()

            pdf.add_page()

            pdf.set_font("Arial", size=12)

            pdf.cell(
                200,
                10,
                txt="Health Report",
                ln=True
            )

            pdf.cell(
                200,
                10,
                txt=f"Generated: {datetime.now()}",
                ln=True
            )

            if not health_df.empty:

                latest = health_df.iloc[-1]

                pdf.cell(
                    200,
                    10,
                    txt=f"Weight: {latest['weight']} kg",
                    ln=True
                )

                pdf.cell(
                    200,
                    10,
                    txt=f"Heart Rate: {latest['heart_rate']}",
                    ln=True
                )

            pdf.output("health_report.pdf")

            with open(
                "health_report.pdf",
                "rb"
            ) as pdf_file:

                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name="health_report.pdf",
                    mime="application/pdf"
                )

            st.success("PDF Generated")

        except Exception as e:
            st.error(f"Error: {e}")

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown("## 🇮🇳 Indian Healthcare Monitoring System")
st.markdown("- Diabetes Monitoring")
st.markdown("- BP Tracking")
st.markdown("- Medication Adherence")
st.markdown("- Health Goal Monitoring")









