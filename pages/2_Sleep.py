import streamlit as st
from src.utils.data_processing import process_sleep_data
from src.components.sleep_visualizations import display_sleep_charts

st.set_page_config(page_title="Sleep Analysis", page_icon="😴", layout="wide")

st.title("Sleep Analysis 😴")

# Get API key from session state
api_key = st.session_state.get('api_key', None)

if api_key:
    col1, col2 = st.columns(2)
    
    with col1:
        # Add date range selector
        date_range = st.select_slider(
            "Select the number of days to display",
            options=range(7, 31),
            value=7,
            help="Choose how many days of historical sleep data to display"
        )
    
    # Add loading state while fetching data
    with st.spinner(f'Fetching your last {date_range} days of sleep data...'):
        sleep_data = process_sleep_data(api_key, date_range)
        display_sleep_charts(sleep_data)
else:
    st.info("Please go back to 'Home' page to connect your Oura Ring.")