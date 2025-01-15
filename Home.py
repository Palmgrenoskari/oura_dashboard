import streamlit as st
from src.utils.api_client import fetch_oura_data, fetch_daily_data
from src.utils.data_processing import process_sleep_data
from src.utils.auth import get_api_key
from src.components.overview import overview_metrics

# Configuration constants
PAGE_TITLE = "Oura Dashboard"
PAGE_HEADER = "Personal Health Analytics"
PAGE_DESCRIPTION = "Welcome to your personal health dashboard. Track your sleep, activity, and readiness metrics from your Oura Ring."
DISCLAIMER = "🚧 Note! This is an MVP (minimum viable product). Expect bugs and incomplete features. 🚧"


def main():
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon="💍",
        layout="wide"
    )
    
    st.title(PAGE_HEADER)
    st.write(PAGE_DESCRIPTION)
    st.caption(DISCLAIMER)
    
    api_key = get_api_key()
    # Store API key in session state
    if api_key:
        st.session_state['api_key'] = api_key
        overview_metrics()

if __name__ == "__main__":
    main()
