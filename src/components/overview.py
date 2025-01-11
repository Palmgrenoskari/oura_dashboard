import streamlit as st
from src.utils.api_client import fetch_oura_data

def load_data(endpoints, data_paths):
    """
    Load required daily data for each endpoint from the Oura API.
    """
    all_data = []
    for i, endpoint in enumerate(endpoints):
        try:
            data = fetch_oura_data(st.session_state['api_key'], endpoint)
            for key in data_paths[i]:
                data = data[key]
            all_data.append(data)
        except Exception:
            all_data.append(None)
            continue
    return all_data

def display_metric(title, icon, value, unit=""):
    if value is not None:   
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
    else:
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
    with st.spinner("Fetching your latest data..."):
        endpoints = ["daily_sleep", "daily_cardiovascular_age", "daily_activity", "daily_resilience", "daily_readiness", "daily_spo2"]
        data_paths = [['data', 0, 'score'], ['data', 0, 'vascular_age'], ['data', 0, 'score'], ['data', 0, 'level'], ['data', 0, 'score'], ['data', 0, 'spo2_percentage', 'average']]
        data = load_data(endpoints, data_paths)
        col1, col2, col3 = st.columns(3)
        with col1:
            display_metric(
                "Sleep Score",
                "😴",
                data[0],
                "pts"
            )
            display_metric(
                "Cardiovascular Age", 
                "💙",
                data[1],
                " years"
            )

        with col2:
            display_metric(
                "Activity Score",
                "🏃‍♂️",
                data[2],
                "pts"
            )
            display_metric(
                "Resilience",
                "💪",
                data[3],
                " level"
            )

        with col3:
            display_metric(
                "Readiness Score",
                "🎯",
                data[4],
                "pts"
            )
            display_metric(
                "Daily AVG SPO2",
                "🩸", 
                data[5],
                "%"
            )