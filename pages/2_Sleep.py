import streamlit as st
from src.utils.data_processing import process_sleep_data
from src.components.sleep_visualizations import display_sleep_charts
from datetime import datetime, timedelta

st.set_page_config(page_title="Sleep Analysis", page_icon="😴", layout="wide")

st.title("Sleep Analysis 😴")

# Get API key from session state
api_key = st.session_state.get('api_key', None)

if api_key:
    col1, col2 = st.columns(2)
    
    with col1:
        # TODO: Add a single day selector
        selected_day = st.date_input(
            "Select the day you want to view", value=datetime.now().date(),
            min_value=datetime(2020, 1, 1).date(),
            max_value=datetime.now().date(),
            help="Select the day to view daily sleep data for, default = last night"
        )
    try:
        with col2:
        # Add date range selector
        
            start_date, end_date = st.date_input(
                "Select date range",
                value=(datetime.now().date().replace(day=1), datetime.now().date()),
                min_value=datetime(2020, 1, 1).date(),
                max_value=datetime.now().date(),
                help="Choose the date range to display sleep data for, default = last 7 days"
            )
            
            # Ensure we have at least the last 7 days of data from today for the averages
            data_start_date = min(selected_day, start_date, (datetime.now().date() - timedelta(days=6)))
            # day count
            day_count = (datetime.now().date() - data_start_date).days + 1
        
    
        # Add loading state while fetching data
        with st.spinner(f'Please wait, fetching your sleep data...'):
            sleep_data = process_sleep_data(api_key, day_count)
            display_sleep_charts(sleep_data, selected_day, start_date, end_date)
    except Exception as e:
        st.info("Please select a valid date range")
else:
    st.info("Please go back to 'Home' page to connect your Oura Ring.")