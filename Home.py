from typing import List, Dict
import streamlit as st
import pandas as pd
from src.utils.api_client import fetch_oura_data
from src.utils.data_processing import process_sleep_data
from src.components.sleep_visualizations import display_sleep_charts

# Configuration constants
PAGE_TITLE = "Oura Dashboard"
PAGE_HEADER = "Personal Health Analytics"
PAGE_DESCRIPTION = "Welcome to your personal health dashboard. Track your sleep, activity, and readiness metrics from your Oura Ring."

def get_api_key():
    """Get API key based on user selection."""
    data_source = st.sidebar.radio(
        "Choose data source",
        ["Use demo data", "Connect Oura Ring"]
    )
    
    if data_source == "Connect Oura Ring":
        user_api_key = st.sidebar.text_input(
            "Enter your Oura API key",
            type="password",
            help="You can find your API key in the Oura web dashboard"
        )
        return user_api_key if user_api_key else None
    return None

def setup_page():
    """Configure initial page settings."""
    st.set_page_config(page_title=PAGE_TITLE, layout="wide")
    st.title(PAGE_HEADER)
    st.write(PAGE_DESCRIPTION)
        
def display_sleep_tab():
    """Render the sleep metrics tab."""
    api_key = get_api_key()
    
    if api_key:
        # Use provided API key
        sleep_data = process_sleep_data(api_key)
        display_sleep_charts(sleep_data)
    else:
        # Use dummy data (to be implemented)
        st.info("Using demo data")
        sleep_data = process_sleep_data()
        display_sleep_charts(sleep_data)

def sleep_view():
    sleep_data = process_sleep_data()
    st.text(sleep_data)

def main():
    """Main application entry point."""
    setup_page()
    
    st.sidebar.header("Data Settings")
    
    tab1, tab2, tab3 = st.tabs(["Sleep","Activity","Readiness"])
    with tab1:
        display_sleep_tab()
    
if __name__ == "__main__":
    main()
