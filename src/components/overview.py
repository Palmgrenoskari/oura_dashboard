import streamlit as st
from src.utils.api_client import fetch_daily_data, fetch_oura_data

def store_age():
    personal_info = fetch_daily_data(st.session_state['api_key'], "personal_info")
    st.session_state['age'] = personal_info['age']

def get_color_code(value, metric_type):
    """Get color based on value and metric type"""
    if value is None:
        return "#888888"
        
    if metric_type == "score":
        if value < 65: return "#FF4B4B"  # Bad - Red
        if value < 70: return "#FFA07A"  # Slightly bad - Light coral
        if value < 80: return "#FFD700"  # Neutral - Gold
        if value < 90: return "#98FB98"  # Good - Pale green
        return "#32CD32"  # Great - Lime green
        
    elif metric_type == "spo2":
        if value < 92: return "#FF4B4B"  # Bad
        if value < 94: return "#FFA07A"  # Slightly bad
        if value < 96: return "#FFD700"  # Neutral  
        if value < 98: return "#98FB98"  # Good
        return "#32CD32"  # Great
        
    elif metric_type == "cardio_age":
        age_diff = value - st.session_state['age']
        if age_diff > 5: return "#FF4B4B"  # Bad
        if age_diff > 3: return "#FFA07A"  # Slightly bad
        if age_diff > -1 and age_diff < 1: return "#FFD700"  # Neutral
        if age_diff > -3: return "#98FB98"  # Good
        return "#32CD32"  # Great
        
    return st.get_option('theme.primaryColor')

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

def display_metric(title, icon, value, unit="", metric_type="score"):
    if value is not None:   
        color = get_color_code(value, metric_type)
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
                        color: {color};
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
        # Store age to compare to cardiovascular age
        store_age()
        endpoints = ["daily_sleep", "daily_cardiovascular_age", "daily_activity", "daily_resilience", "daily_readiness", "daily_spo2"]
        data_paths = [['data', 0, 'score'], ['data', 0, 'vascular_age'], ['data', 0, 'score'], ['data', 0, 'level'], ['data', 0, 'score'], ['data', 0, 'spo2_percentage', 'average']]
        data = load_data(endpoints, data_paths)
        col1, col2, col3 = st.columns(3)
        with col1:
            display_metric(
                "Sleep Score",
                "😴",
                data[0],
                "pts",
                "score"
            )
            display_metric(
                "Cardiovascular Age", 
                "💙",
                data[1],
                " years",
                "cardio_age"
            )

        with col2:
            display_metric(
                "Activity Score",
                "🏃‍♂️",
                data[2],
                "pts",
                "score"
            )
            display_metric(
                "Resilience",
                "💪",
                data[3],
                " level",
                "score"
            )

        with col3:
            display_metric(
                "Readiness Score",
                "🎯",
                data[4],
                "pts",
                "score"
            )
            display_metric(
                "Daily AVG SPO2",
                "🩸", 
                data[5],
                "%",
                "spo2"
            )