mport streamlit as st
import pandas as pd
import random


# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="AI Timetable Generator",
    layout="wide"
)



# ---- CUSTOM CSS ----
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #f5f5f5;
        font-family: 'Poppins', sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #aee6ff;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        margin-bottom: 1rem;
    }

    .subheader {
        text-align: center;
        font-size: 1.2rem;
        color: #00000f;
        margin-bottom: 2rem;
    }


    

    .stButton > button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: 0.3s;
        box-shadow: 0px 0px 10px rgba(0, 150, 255, 0.5);
    }

    

    .stButton > button:hover {
        background: linear-gradient(90deg, #38ef7d, #11998e);
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(56, 239, 125, 0.7);
    }

    

    .dataframe th {
        background-color: #1c2541 !important;
        color: #aee6ff !important;
        text-align: center;
    }



    .dataframe td {
        background-color: #3a506b !important;
        color: #f5f5f5 !important;
        text-align: center;
    }

    .footer {
        text-align: center;
        color: #aee6ff;
        font-size: 0.9rem;
        margin-top: 3rem;
        opacity: 0.8;
    }
    </style>
""", unsafe_allow_html=True)



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
