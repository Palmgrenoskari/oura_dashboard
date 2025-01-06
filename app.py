import streamlit as st

st.set_page_config(page_title="Oura Dashboard", layout="wide")

st.title("Personal Health Analytics")

st.write("Welcome to your personal health dashboard. Track your sleep, activity, and readiness metrics from your Oura Ring.")

st.markdown("---")

# Create tabs for different graph categories
tab1, tab2, tab3 = st.tabs(["Sleep", "Activity", "Readiness"])

with tab1:
    st.subheader("Sleep Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sleep Time", "7h 23m")
        st.line_chart(
            {"Sleep Duration": [7.5, 6.8, 8.1, 7.2, 7.4, 6.9, 7.8]},
            height=200
        )
    
    with col2:
        st.metric("Sleep Score", "85")
        st.line_chart(
            {"Sleep Score": [85, 82, 88, 79, 86, 83, 87]},
            height=200
        )
    
    with col3:
        st.metric("Deep Sleep", "1h 45m")
        st.metric("REM Sleep", "1h 30m")
        st.metric("Sleep Latency", "12 min")
        st.metric("Sleep Efficiency", "92%")

with tab2:
    st.subheader("Activity Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Daily Steps", "8,742")
        st.bar_chart(
            {"Steps": [8742, 10123, 7865, 9234, 8654, 11234, 9876]},
            height=200
        )
    
    with col2:
        st.metric("Activity Score", "78")
        st.line_chart(
            {"Activity Score": [78, 82, 75, 80, 77, 85, 79]},
            height=200
        )
    
    with col3:
        st.metric("Calories Burned", "2,450")
        st.metric("Walking Equivalent", "6.2 km")
        st.metric("Training Frequency", "4/7 days")
        st.metric("Movement", "85%")

with tab3:
    st.subheader("Readiness Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("HRV", "45 ms")
        st.area_chart(
            {"HRV": [45, 48, 42, 46, 44, 47, 43]},
            height=200
        )
    
    with col2:
        st.metric("Resting Heart Rate", "62 bpm")
        st.line_chart(
            {"Resting HR": [62, 60, 63, 61, 64, 62, 61]},
            height=200
        )
    
    with col3:
        st.metric("Temperature Deviation", "+0.2°C")
        st.metric("Recovery Index", "88")
        st.metric("Body Battery", "75%")
        st.metric("Respiratory Rate", "14 rpm")
