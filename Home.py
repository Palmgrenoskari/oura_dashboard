import streamlit as st
from src.utils.api_client import fetch_oura_data
from src.utils.data_processing import process_sleep_data
import time

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

def display_metric(title, icon, endpoint, data_path, unit=""):
    try:
        data = fetch_oura_data(st.session_state['api_key'], endpoint, 1)
        value = data
        for key in data_path:
            value = value[key]
            
        # Create a custom container with CSS styling
        with st.container():
            st.markdown(f"""
                <div style="
                    background-color: {st.get_option('theme.secondaryBackgroundColor')};
                    padding: 1rem;
                    border-radius: 0.5rem;
                    margin-bottom: 1rem;
                    min-height: 120px;
                    width: 100%;
                ">
                    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                        {icon} {title}
                    </div>
                    <div style="
                        font-size: 2rem;
                        font-weight: bold;
                        color: {st.get_option('theme.primaryColor')};
                    ">
                        {value}{unit}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        with st.container():
            st.markdown(f"""
                <div style="
                    background-color: {st.get_option('theme.secondaryBackgroundColor')};
                    padding: 1rem;
                    border-radius: 0.5rem;
                    margin-bottom: 1rem;
                    opacity: 0.7;
                    min-height: 122px;
                    width: 100%;
                ">
                    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                        {icon} {title}
                    </div>
                    <div style="color: #888888;">
                        No data available
                    </div>
                </div>
            """, unsafe_allow_html=True)

def overview_metrics():
    
    # Display overview metrics
    st.header("Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        display_metric(
            "Sleep Score",
            "😴",
            "daily_sleep",
            ['data', 0, 'score'],
            "pts"
        )
        display_metric(
            "Cardiovascular Age", 
            "💙",
            "daily_cardiovascular_age",
            ['data', 0, 'vascular_age'],
            " years"
        )

    with col2:
        display_metric(
            "Activity Score",
            "🏃‍♂️",
            "daily_activity",
            ['data', 0, 'score'],
            "pts"
        )
        display_metric(
            "Resilience",
            "💪",
            "daily_resilience", 
            ['data', 0, 'level']
        )

    with col3:
        display_metric(
            "Readiness Score",
            "🎯",
            "daily_readiness",
            ['data', 0, 'score'],
            "pts"
        )
        display_metric(
            "Daily AVG SPO2",
            "🩸", 
            "daily_spo2",
            ['data', 0, 'spo2_percentage', 'average'],
            "%"
        )

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
        
        overview_metrics()

if __name__ == "__main__":
    main()
