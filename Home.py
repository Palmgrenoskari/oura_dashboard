from typing import List, Dict
import streamlit as st
import pandas as pd
from src.utils.api_client import fetch_oura_data
from src.utils.data_processing import process_sleep_data
from src.components.sleep_visualizations import display_sleep_charts

# Access secrets
API_KEY = st.secrets["OURA_API_KEY"]

# Configuration constants
PAGE_TITLE = "Oura Dashboard"
PAGE_HEADER = "Personal Health Analytics"
PAGE_DESCRIPTION = "Welcome to your personal health dashboard. Track your sleep, activity, and readiness metrics from your Oura Ring."

def setup_page():
    """Configure initial page settings."""
    st.set_page_config(page_title=PAGE_TITLE, layout="wide")
    st.title(PAGE_HEADER)
    st.write(PAGE_DESCRIPTION)

def display_sleep_tab():
    """Render the sleep metrics tab."""
    sleep_data = process_sleep_data()
    display_sleep_charts(sleep_data)

def sleep_view():
    sleep_data = process_sleep_data()
    st.text(sleep_data)

def main():
    """Main application entry point."""
    setup_page()
    tab1, tab2, tab3 = st.tabs(["Sleep","Activity","Readiness"])
    with tab1:
        display_sleep_tab()
    
    st.sidebar.header("Sidebar")
    st.sidebar.text("This is the sidebar")
    
if __name__ == "__main__":
    main()
