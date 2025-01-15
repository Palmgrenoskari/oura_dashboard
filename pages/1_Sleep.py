import streamlit as st
from src.utils.data_processing import process_sleep_data, load_sleep_data
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
    with col2:
    # Add date range selector
    
        date_range = st.date_input(
            "Select date range",
            value=(datetime.now().date().replace(day=1), datetime.now().date()),
            min_value=datetime(2020, 1, 1).date(),
            max_value=datetime.now().date(),
            help="Choose the date range to display sleep data for, default = last 7 days"
        )
        
        # Check if both dates are selected
        if len(date_range) != 2:
            _, col2b = st.columns(2)
            with col2b:
                st.info("Please select both a start and end date")
            st.stop()
            
        start_date, end_date = date_range
        
        # Ensure we have at least the last 7 days of data from today for the averages
        data_start_date = min(selected_day, start_date, (datetime.now().date() - timedelta(days=6)))
        # day count
        day_count = (datetime.now().date() - data_start_date).days + 1
    

    # Add loading state while fetching data
    with st.spinner(f'Please wait, fetching your sleep data...'):
        sleep_data = process_sleep_data(api_key, day_count)
        display_sleep_charts(sleep_data, selected_day, start_date, end_date)
else:
    st.info("Note! Using demo data. Data is only available for days between 2025-01-02 and 2025-01-15")
    col1, col2 = st.columns(2)
    
    with col1:
        selected_day = st.date_input(
            "Select day", value=datetime(2025, 1, 15).date(),
            min_value=datetime(2025, 1, 2).date(),
            max_value=datetime(2025, 1, 15).date(),
            help="Select the day to view daily sleep data for, default = Jan 15th 2025"
        )
    with col2:
    # Add date range selector
    
        date_range = st.date_input(
            "Select date range",
            value=(datetime(2025, 1, 2).date(), datetime(2025, 1, 15).date()),
            min_value=datetime(2025, 1, 2).date(),
            max_value=datetime(2025, 1, 15).date(),
            help="Choose the date range to display sleep data for, default = Jan 2nd 2025 - Jan 15th 2025"
        )
        
        # Check if both dates are selected
        if len(date_range) != 2:
            _, col2b = st.columns(2)
            with col2b:
                st.info("Please select both a start and end date")
            st.stop()
            
        start_date, end_date = date_range
        
    

    # Add loading state while fetching data
    with st.spinner(f'Please wait, fetching your sleep data...'):
        sleep_data = load_sleep_data()
        display_sleep_charts(sleep_data, selected_day, start_date, end_date)