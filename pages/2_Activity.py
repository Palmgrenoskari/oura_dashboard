import streamlit as st
from src.utils.data_processing import process_activity_data
from src.components.activity_visualizations import display_activity_charts
from datetime import datetime, timedelta

st.set_page_config(page_title="Activity Analysis", page_icon="🏃‍♂️", layout="wide")
        
st.title("Activity Tracking 🏃‍♂️")

api_key = st.session_state.get('api_key', None)
if api_key:
    col1, col2 = st.columns(2)
    
    with col1:
        selected_day = st.date_input(
            "Select the day you want to view", value=datetime.now().date(),
            min_value=datetime(2020, 1, 1).date(),
            max_value=datetime.now().date(),
            help="Select the day to view daily activity data for, default = today"
        )
    try:
        with col2:
        # Add date range selector
        
            start_date, end_date = st.date_input(
                "Select date range",
                value=(datetime.now().date().replace(day=1), datetime.now().date()),
                min_value=datetime(2020, 1, 1).date(),
                max_value=datetime.now().date(),
                help="Choose the date range to display activity data for, default = last 7 days"
            )
            
            # Ensure we have at least the last 7 days of data from today for the averages
            data_start_date = min(selected_day, start_date, (datetime.now().date() - timedelta(days=6)))
            # day count
            day_count = (datetime.now().date() - data_start_date).days + 1
        with st.spinner(f'Please wait, fetching your activity data...'):
            activity_df = process_activity_data(api_key, day_count)  # Get 30 days of data
            display_activity_charts(activity_df, selected_day, start_date, end_date)
    except Exception as e:
        st.info("Please select a valid date range")
else:
    st.info("Please set up your API key in the Home page.")