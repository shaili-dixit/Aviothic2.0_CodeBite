mport streamlit as st
import pandas as pd
import random

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="AI Timetable Generator",
    layout="wide"
)
# ---- HEADER ----
st.markdown('<h1 class="main-title"> AI Timetable Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Generate 10 smart, personalized weekly timetables using AI<br>(Priority = Subjects you want before lunch)</p>', unsafe_allow_html=True)

# ---- INPUT SECTION ----
col1, col2 = st.columns(2)

with col1:
    subjects_input = st.text_input("Enter your subjects (comma-separated):", placeholder="e.g., Math, Science, English, History")
    total_periods = st.number_input("Total number of periods per day:", 4, 10, 6)
    total_days = st.number_input("Number of working days per week:", 3, 7, 5)
    lunch_time = st.text_input("Enter fixed lunch time (e.g., 1:00 PM - 2:00 PM):", "1:00 PM - 2:00 PM")

with col2:
    st.write("### Set Priorities and Weekly Periods per Subject")
    st.caption("Higher priority = earlier (before lunch). Enter how many periods per week per subject.")
    subject_data = []

    if subjects_input:
        subjects = [s.strip() for s in subjects_input.split(",") if s.strip()]
        for subject in subjects:
            col_a, col_b = st.columns(2)
            with col_a:
                priority = st.slider(
                    f"Priority for {subject}",
                    1, 5, 3,
                    key=f"priority_{subject}"  # ✅ unique key
                )
            with col_b:
                periods = st.number_input(
                    f"Weekly periods for {subject}",
                    1, total_days * total_periods, 3,
                    key=f"periods_{subject}"  # ✅ unique key
                )
            subject_data.append({"subject": subject, "priority": priority, "periods": periods})
