from typing import List, Dict
import streamlit as st
from src.utils.api_client import fetch_oura_data
from src.utils.data_processing import process_sleep_data

# Access secrets
API_KEY = st.secrets["OURA_API_KEY"]

# Configuration constants
PAGE_TITLE = "Oura Dashboard"
PAGE_HEADER = "Personal Health Analytics"
PAGE_DESCRIPTION = "Welcome to your personal health dashboard. Track your sleep, activity, and readiness metrics from your Oura Ring."

# Sample data - In real app, this would come from a data service
SAMPLE_DATA = {
    "sleep": {
        "total_time": "7h 23m",
        "score": "85",
        "deep_sleep": "1h 45m",
        "rem_sleep": "1h 30m",
        "latency": "12 min",
        "efficiency": "92%",
        "duration_history": [7.5, 6.8, 8.1, 7.2, 7.4, 6.9, 7.8],
        "score_history": [85, 82, 88, 79, 86, 83, 87]
    },
    "activity": {
        "steps": "8,742",
        "score": "78",
        "calories": "2,450",
        "walking_equiv": "6.2 km",
        "training_freq": "4/7 days",
        "movement": "85%",
        "steps_history": [8742, 10123, 7865, 9234, 8654, 11234, 9876],
        "score_history": [78, 82, 75, 80, 77, 85, 79]
    },
    "readiness": {
        "hrv": "45 ms",
        "resting_hr": "62 bpm",
        "temp_deviation": "+0.2°C",
        "recovery_index": "88",
        "body_battery": "75%",
        "respiratory_rate": "14 rpm",
        "hrv_history": [45, 48, 42, 46, 44, 47, 43],
        "hr_history": [62, 60, 63, 61, 64, 62, 61]
    }
}

def setup_page() -> None:
    """Configure initial page settings."""
    st.set_page_config(page_title=PAGE_TITLE, layout="wide")
    st.title(PAGE_HEADER)
    st.write(PAGE_DESCRIPTION)
    st.markdown("---")

def display_metrics_column(metrics: Dict[str, str]) -> None:
    """Display a column of metrics.
    
    Args:
        metrics: Dictionary of metric labels and values
    """
    for label, value in metrics.items():
        st.metric(label, value)

def display_sleep_tab(data: Dict) -> None:
    """Render the sleep metrics tab."""
    st.subheader("Sleep Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sleep Time", data["total_time"])
        st.line_chart(
            {"Sleep Duration": data["duration_history"]},
            height=200
        )
    
    with col2:
        st.metric("Sleep Score", data["score"])
        st.line_chart(
            {"Sleep Score": data["score_history"]},
            height=200
        )
    
    with col3:
        display_metrics_column({
            "Deep Sleep": data["deep_sleep"],
            "REM Sleep": data["rem_sleep"],
            "Sleep Latency": data["latency"],
            "Sleep Efficiency": data["efficiency"]
        })

def display_activity_tab(data: Dict) -> None:
    """Render the activity metrics tab."""
    st.subheader("Activity Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Daily Steps", data["steps"])
        st.bar_chart(
            {"Steps": data["steps_history"]},
            height=200
        )
    
    with col2:
        st.metric("Activity Score", data["score"])
        st.line_chart(
            {"Activity Score": data["score_history"]},
            height=200
        )
    
    with col3:
        display_metrics_column({
            "Calories Burned": data["calories"],
            "Walking Equivalent": data["walking_equiv"],
            "Training Frequency": data["training_freq"],
            "Movement": data["movement"]
        })

def display_readiness_tab(data: Dict) -> None:
    """Render the readiness metrics tab."""
    st.subheader("Readiness Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("HRV", data["hrv"])
        st.area_chart(
            {"HRV": data["hrv_history"]},
            height=200
        )
    
    with col2:
        st.metric("Resting Heart Rate", data["resting_hr"])
        st.line_chart(
            {"Resting HR": data["hr_history"]},
            height=200
        )
    
    with col3:
        display_metrics_column({
            "Temperature Deviation": data["temp_deviation"],
            "Recovery Index": data["recovery_index"],
            "Body Battery": data["body_battery"],
            "Respiratory Rate": data["respiratory_rate"]
        })

def main() -> None:
    """Main application entry point."""
    setup_page()
    
    sleep_data = process_sleep_data()
    
    for day in sleep_data['data']:
        st.header(day['id'])
        st.text(day)
        # st.text_input('average_breath', day['average_breath'])
        # st.text_input('average_hr', day['average_heart_rate'])
        # st.text_input('average_hrv', day['average_hrv'])
        # st.text_input('awake_time', day['awake_time'])
        # st.text_input('bedtime_end', day['bedtime_end'])
        # st.text_input('bedtime_start', day['bedtime_start'])
        # st.text_input('day', day['day'])
        # st.text_input('deep_sleep_duration', day['deep_sleep_duration'])
        # st.text_input('efficiency', day['efficiency'])
        # st.text_input('latency', day['latency'])
        # st.text_input('light_sleep_duration', day['light_sleep_duration'])
        # st.text_input('low_battery_alert', day['low_battery_alert'])
        # st.text_input('lowest_heart_rate', day['lowest_heart_rate'])
        # st.text_input('period', day['period'])
        # st.text_input('rem_sleep_duration', day['rem_sleep_duration'])
        # st.text_input('restless_periods', day['restless_periods'])
        # st.text_input('sleep_algorithm_version', day['sleep_algorithm_version'])
        # st.text_input('time_in_bed', day['time_in_bed'])
        # st.text_input('total_sleep_duration', day['total_sleep_duration'])
        # st.text_input('type', day['type'])
    
    st.sidebar.header("Sidebar")
    st.sidebar.text("This is the sidebar")
    
    st.header("Sample Data:")
    # Create tabs for different graph categories
    tab1, tab2, tab3 = st.tabs(["Sleep", "Activity", "Readiness"])
    
    with tab1:
        display_sleep_tab(SAMPLE_DATA["sleep"])
    
    with tab2:
        display_activity_tab(SAMPLE_DATA["activity"])
    
    with tab3:
        display_readiness_tab(SAMPLE_DATA["readiness"])

if __name__ == "__main__":
    main()
