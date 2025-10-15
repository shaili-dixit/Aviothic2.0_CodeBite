# app.py
import streamlit as st
import pandas as pd
import random
from collections import defaultdict

# --------------------------
# Page config & CSS (Dark Elegant)
# --------------------------
st.set_page_config(page_title="AI Timetable Generator", layout="wide")

st.markdown("""
    <style>
    * {
        font-family: 'Poppins', sans-serif;
    }

    body {
        background: #ffffff;
        color: #111;
    }

    .block-container {
        padding: 1.5rem 2rem !important;
    }

    /* Title with dark gradient */
    .title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }

    .subtitle {
        text-align: center;
        color: #333;
        font-size: 1.1rem;
        margin-bottom: 1.8rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
        color: #f1f1f1;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #141e30, #243b55);
        color: #ffffff !important;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: 0.3s ease;
        box-shadow: 0 0 10px rgba(36, 59, 85, 0.4);
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #283e51, #485563);
        transform: translateY(-2px);
        box-shadow: 0 0 18px rgba(0,0,0,0.5);
    }

    /* Tables */
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden;
        border: 2px solid #1a1a1a;
        margin-top: 10px;
    }

    .dataframe th {
        background: linear-gradient(90deg, #232526, #414345) !important;
        color: #f8f8f8 !important;
        padding: 10px !important;
        text-align: center;
    }

    .dataframe td {
        background-color: #f5f5f5 !important;
        color: #111 !important;
        text-align: center;
        padding: 8px !important;
        border-bottom: 1px solid #ddd;
    }

    .dataframe td:hover {
        background-color: #e8e8e8 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #f2f2f2;
        border-radius: 10px;
        padding: 6px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #232526, #414345);
        color: white !important;
        border-radius: 8px;
    }

    .footer {
        text-align: center;
        color: #333;
        margin-top: 2rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">AI Timetable Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Dark Modern UI | Student & Faculty Timetables</div>', unsafe_allow_html=True)

# --------------------------
# Sidebar mode selector
# --------------------------
mode = st.sidebar.selectbox("Choose Module", ["Student Timetable", "Faculty Timetable", "About / Help"])

# --------------------------
# Helper: Styled HTML Table
# --------------------------
def styled_html_table(df, caption=None):
    styled = df.style.set_table_styles([
        {"selector": "thead th", "props": [
            ("background", "linear-gradient(90deg, #232526, #414345)"),
            ("color", "#f8f8f8"), ("font-weight", "700"), ("text-align", "center")
        ]},
        {"selector": "tbody td", "props": [
            ("background-color", "#f5f5f5"),
            ("color", "#111"), ("padding", "8px"), ("text-align", "center")
        ]},
        {"selector": "tbody tr:hover td", "props": [
            ("background-color", "#e8e8e8")
        ]},
        {"selector": "table", "props": [
            ("border-collapse", "collapse"),
            ("margin", "auto"),
            ("border-radius", "10px"),
            ("overflow", "hidden"),
            ("box-shadow", "0 4px 20px rgba(0,0,0,0.1)")
        ]}
    ])
    if caption:
        styled = styled.set_caption(caption)
    return styled.to_html(escape=False)

# --------------------------
# Student Timetable Module
# --------------------------
if mode == "Student Timetable":
    st.header("Student Timetable Generator")

    col1, col2 = st.columns(2)
    with col1:
        subjects_input = st.text_input("Enter your subjects (comma-separated):", placeholder="Math, Science, English")
        total_periods = st.number_input("Periods per day", 4, 10, 6)
        total_days = st.number_input("Working days per week", 3, 7, 5)
    with col2:
        lunch_period = st.number_input("Lunch Period (1-indexed):", 1, 10, (total_periods // 2) + 1)
        st.caption("Priority: Lower number = earlier before lunch.")

    subject_data = []
    if subjects_input:
        subjects = [s.strip() for s in subjects_input.split(",") if s.strip()]
        st.subheader("Subject Priorities & Weekly Periods")
        for s in subjects:
            c1, c2 = st.columns([2, 1])
            with c1:
                p = st.slider(f"Priority for {s}", 1, 5, 3)
            with c2:
                per = st.number_input(f"Periods/week for {s}", 1, total_days * total_periods, 3)
            subject_data.append({"subject": s, "priority": p, "periods": per})

    def make_student_timetable(data, days, periods, lunch_idx):
        data.sort(key=lambda x: x["priority"])
        expanded = [s["subject"] for s in data for _ in range(s["periods"])]
        total_slots = days * periods
        expanded.extend(["Free / Revision"] * max(0, total_slots - len(expanded)))
        random.shuffle(expanded)

        week = {f"Day {d+1}": [] for d in range(days)}
        idx = 0
        for d in range(days):
            for p in range(1, periods + 1):
                if p == lunch_idx:
                    week[f"Day {d+1}"].append(" Lunch Break")
                else:
                    week[f"Day {d+1}"].append(expanded[idx] if idx < len(expanded) else "Free / Revision")
                    idx += 1
        df = pd.DataFrame(week)
        df.index = [f"Period {i}" for i in range(1, periods + 1)]
        return df

    if st.button("Generate 10 Student Timetables"):
        if not subject_data:
            st.warning("Please enter subjects first.")
        else:
            tabs = st.tabs([f"Timetable {i+1}" for i in range(10)])
            for i, tab in enumerate(tabs):
                with tab:
                    df = make_student_timetable(subject_data, total_days, total_periods, lunch_period)
                    st.markdown(styled_html_table(df, caption=f"Student Timetable #{i+1}"), unsafe_allow_html=True)
            st.success("Generated 10 Student Timetables successfully!")

# --------------------------
# Faculty Timetable Module
# --------------------------
elif mode == "Faculty Timetable":
    st.header("Faculty Timetable Generator")

    col1, col2 = st.columns(2)
    with col1:
        subs = st.text_input("Enter subjects:", placeholder="Physics, Chemistry, Math")
        total_periods = st.number_input("Periods per day", 4, 10, 6)
        total_days = st.number_input("Working days", 3, 7, 5)
    with col2:
        lunch_period = st.number_input("Lunch Period:", 1, 10, (total_periods // 2) + 1)
        st.caption("Each subject must have a faculty assigned.")

    subject_data = []
    if subs:
        subjects = [s.strip() for s in subs.split(",") if s.strip()]
        for sub in subjects:
            c1, c2 = st.columns([2, 1])
            with c1:
                f = st.text_input(f"Faculty for {sub}", placeholder="e.g., Sanjana Kanaujiya")
            with c2:
                p = st.number_input(f"Weekly periods for {sub}", 1, total_days * total_periods, 3)
            if f:
                subject_data.append({"subject": sub, "faculty": f, "periods": p})

    def build_faculty_timetables(data, days, periods, lunch_idx):
        instances = [(s["subject"], s["faculty"]) for s in data for _ in range(s["periods"])]
        total_slots = days * periods
        if len(instances) > total_slots:
            instances = instances[:total_slots]

        week = {f"Day {d+1}": [""] * periods for d in range(days)}
        for d in range(days):
            week[f"Day {d+1}"][lunch_idx - 1] = "Lunch Break"

        bookings = defaultdict(set)
        slots = [(d, p) for d in range(days) for p in range(1, periods + 1) if p != lunch_idx]
        random.shuffle(instances)
        random.shuffle(slots)

        for sub, fac in instances:
            for d, p in slots:
                if (d, p) not in bookings[fac]:
                    week[f"Day {d+1}"][p - 1] = f"{sub} ({fac})"
                    bookings[fac].add((d, p))
                    slots.remove((d, p))
                    break

        for d in range(days):
            for p in range(periods):
                if week[f"Day {d+1}"][p] == "":
                    week[f"Day {d+1}"][p] = "Free / Revision"

        df = pd.DataFrame(week)
        df.index = [f"Period {i}" for i in range(1, periods + 1)]

        faculty_tables = {}
        for fac in set([s["faculty"] for s in data]):
            f_week = {f"Day {d+1}": [] for d in range(days)}
            for d in range(days):
                for p in range(periods):
                    cell = df.iloc[p, d]
                    if f"({fac})" in cell:
                        f_week[f"Day {d+1}"].append(cell.split(" (")[0])
                    elif cell == "Lunch Break":
                        f_week[f"Day {d+1}"].append("Lunch Break")
                    else:
                        f_week[f"Day {d+1}"].append("Free / No Class")
            faculty_tables[fac] = pd.DataFrame(f_week, index=[f"Period {i}" for i in range(1, periods + 1)])
        return df, faculty_tables

    if st.button("Generate Faculty Timetables"):
        if not subject_data:
            st.warning("Please fill all faculty details.")
        else:
            student_df, faculty_tables = build_faculty_timetables(subject_data, total_days, total_periods, lunch_period)
            st.markdown(styled_html_table(student_df, caption="Student Timetable (with Faculty)"), unsafe_allow_html=True)
            tabs = st.tabs(list(faculty_tables.keys()))
            for i, f in enumerate(faculty_tables.keys()):
                with tabs[i]:
                    st.markdown(styled_html_table(faculty_tables[f], caption=f"{f}'s Timetable"), unsafe_allow_html=True)
            st.success("Faculty Timetables generated successfully!")

# --------------------------
# About Tab
# --------------------------
else:
    st.header("ℹ️ About This App")
    st.markdown("""
    - **Student Timetable:** Create 10 AI-randomized timetables with subject priorities.
    - **Faculty Timetable:** Assign teachers, generate both student & per-faculty timetables automatically.
    - All timetables include fixed lunch breaks & non-overlapping schedules.
    - Designed for hackathons, schools & smart institutions.

      Developed by **Team CodeBite**  
    Members: **Sanjana Kanaujiya**, **Rashi Shukla**, **Tanuvanshi Shukla**, **Shaili Dixit**
    """)

st.markdown('<div class="footer">© 2025 Team CodeBite | AI Timetable Generator</div>', unsafe_allow_html=True)
