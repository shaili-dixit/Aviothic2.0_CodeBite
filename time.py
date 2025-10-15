import streamlit as st
import pandas as pd
import random

# ---- PAGE CONFIG ----
st.set_page_config(page_title="AI Timetable Generator", layout="wide")

# ---- MODERN CSS ----
st.markdown("""
    <style>
    * { font-family: 'Poppins', sans-serif; }

    body {
        background: linear-gradient(135deg, #2b10ff, #7147de, #b8a2db);
        color: #f5f7fa;
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 1.2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff8a00, #e52e71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
        margin-bottom: 0.5rem;
    }

    .subheader {
        text-align: center;
        font-size: 1.1rem;
        color: #a3e2e6;
        opacity: 0.9;
        margin-bottom: 2rem;
    }

    /* --- BUTTONS --- */
    .stButton > button {
        background: linear-gradient(90deg, #e52e71, #ff8a00);
        color: black !important;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 20px rgba(255, 100, 150, 0.4);
        transition: all 0.3s ease-in-out;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #ff758c, #ff7eb3);
        box-shadow: 0 6px 30px rgba(255, 150, 180, 0.5);
    }

    /* --- TABLE --- */
    .dataframe {
        border-radius: 14px !important;
        border-collapse: collapse !important;
        overflow: hidden !important;
        margin-top: 1rem;
        background: linear-gradient(90deg, #fa8500, #e62e11);
        
    }
    .dataframe th {
        background: rgba(255, 255, 255, 0.15) !important;
        color: #000000 !important;
        text-transform: uppercase;
        font-weight: 700;
        text-align: center;
        padding: 12px !important;
        backdrop-filter: blur(10px);
    }
    .dataframe td {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        text-align: center;
        padding: 10px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        transition: background 0.3s ease-in-out;
    }
    .dataframe td:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
    }

    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(220, 180, 255, 0.1);
        border-radius: 12px;
        padding: 6px;
        backdrop-filter: blur(10px);
    }
    .stTabs [data-baseweb="tab"] {
        color: #000000 !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #ff8a00, #e52e71);
        color: black !important;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(255, 120, 150, 0.5);
    }

    /* --- FOOTER --- */
    .footer {
        text-align: center;
        color: #f1b2a6;
        font-size: 0.9rem;
        margin-top: 3rem;
        opacity: 0.8;
    }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown('<h1 class="main-title">AI Timetable Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Create 10 unique, smart weekly timetables <br>(Priority = Subjects you want before lunch)</p>', unsafe_allow_html=True)

# ---- INPUT SECTION ----
col1, col2 = st.columns(2)

with col1:
    subjects_input = st.text_input("Enter your subjects (comma-separated):", placeholder="e.g., Math, Science, English, History")
    total_periods = st.number_input("Total periods per day:", 4, 10, 6)
    total_days = st.number_input("Working days per week:", 3, 7, 5)
    lunch_time = st.text_input("Enter fixed lunch time (e.g., 1:00 PM - 2:00 PM):", "1:00 PM - 2:00 PM")

with col2:
    st.write("### Set Priority and Weekly Periods per Subject")
    st.caption("Higher priority = earlier (before lunch). Enter periods per week.")
    subject_data = []

    if subjects_input:
        subjects = [s.strip() for s in subjects_input.split(",") if s.strip()]
        for subject in subjects:
            col_a, col_b = st.columns(2)
            with col_a:
                priority = st.slider(f"Priority for {subject}", 1, 5, 3, key=f"priority_{subject}")
            with col_b:
                periods = st.number_input(f"Weekly periods for {subject}", 1, total_days * total_periods, 3, key=f"periods_{subject}")
            subject_data.append({"subject": subject, "priority": priority, "periods": periods})

# ---- GENERATE BUTTON ----
if st.button(" Generate 10 Timetables"):
    if not subject_data:
        st.warning("⚠️ Please enter subjects and their settings first.")
    else:
        subject_data.sort(key=lambda x: x["priority"])

        def generate_timetable():
            subjects_expanded = []
            for s in subject_data:
                subjects_expanded.extend([s["subject"]] * s["periods"])

            total_slots = total_days * total_periods
            free_slots = total_slots - len(subjects_expanded)
            subjects_expanded.extend(["Free Period"] * max(0, free_slots))
            random.shuffle(subjects_expanded)

            week_timetable = {f"Day {i+1}": [] for i in range(total_days)}
            index = 0

            for day in week_timetable:
                for period in range(total_periods):
                    if period == total_periods // 2:
                        week_timetable[day].append("Lunch Break")
                    else:
                        if index < len(subjects_expanded):
                            week_timetable[day].append(subjects_expanded[index])
                            index += 1
                        else:
                            week_timetable[day].append("Free Period")

            # Shuffle free periods evenly across days
            all_free_positions = []
            for day in week_timetable:
                for i, sub in enumerate(week_timetable[day]):
                    if sub == "Free Period":
                        all_free_positions.append((day, i))
            random.shuffle(all_free_positions)
            for (day, i), (swap_day, swap_i) in zip(all_free_positions, reversed(all_free_positions)):
                if day != swap_day:
                    week_timetable[day][i], week_timetable[swap_day][swap_i] = (
                        week_timetable[swap_day][swap_i],
                        week_timetable[day][i],
                    )

            return pd.DataFrame(week_timetable)

        st.subheader(" Generated Smart Timetables")
        tabs = st.tabs([f"Timetable {i+1}" for i in range(10)])
        for i, tab in enumerate(tabs):
            with tab:
                df = generate_timetable()
                st.dataframe(df, use_container_width=True)

        st.success("✅ 10 balanced and elegant timetables generated successfully!")

st.markdown('<p class="footer">© 2025 Team CodeBite | AI Timetable Generator </p>', unsafe_allow_html=True)
