import streamlit as st
from src.utils.api_client import fetch_oura_data
from src.utils.data_processing import process_sleep_data

# Configuration constants
PAGE_TITLE = "Oura Dashboard"
PAGE_HEADER = "Personal Health Analytics"
PAGE_DESCRIPTION = "Welcome to your personal health dashboard. Track your sleep, activity, and readiness metrics from your Oura Ring."

def get_api_key():
    """Get API key based on user selection."""
    data_source = st.radio(
        "Choose data source",
        ["Use demo data", "Connect Oura Ring"]
    )
    
    if data_source == "Connect Oura Ring":
        user_api_key = st.text_input(
            "Enter your Oura API key",
            type="password",
            help="You can find your API key in the Oura web dashboard",
            key="api_key_input"
        )
        
        if user_api_key:
            st.success("API key successfully added! ✅")
            return user_api_key
        return None
    elif data_source == "Use demo data":
        return st.secrets["OURA_API_KEY"]
    return None

def main():
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon="💍",
        layout="wide"
    )
    
    st.title(PAGE_HEADER)
    st.write(PAGE_DESCRIPTION)
    
    api_key = get_api_key()
    # Store API key in session state
    if api_key:
        st.session_state['api_key'] = api_key
    
    # Display overview metrics
    st.header("Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("Sleep Score", icon="😴")
    with col2:
        st.info("Activity Score", icon="🏃‍♂️")
    with col3:
        st.info("Readiness Score", icon="🎯")
    
    st.markdown("""
    ### Navigate to specific pages:
    - **Sleep**: Detailed sleep analysis and trends
    - **Activity**: Activity metrics and movement data
    - **Extra**: Additional insights and analytics
    """)

if __name__ == "__main__":
    main()
