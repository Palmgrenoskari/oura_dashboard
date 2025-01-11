import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from src.utils.data_processing import process_activity_data
from src.utils.auth import get_api_key

st.set_page_config(page_title="Activity Analysis", page_icon="🏃‍♂️", layout="wide")

def display_activity_charts(activity_df):
    # Create two columns
    col1, col2 = st.columns(2)

    # 1. Activity Metrics
    with col1:
        st.subheader("Activity Metrics")
        latest = activity_df.iloc[-1]
        
        # Calculate weekly averages
        weekly_avg = activity_df.tail(7).mean(numeric_only=True)
        
        # Create custom metric display function
        def custom_metric(label, value, avg_text):
            return f"""
                <div style="margin-bottom: 1rem;">
                    <div style="font-size: 1rem; margin-bottom: 0.2rem;">{label}</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{value}</div>
                    <div style="font-size: 0.8rem; color: #808495;">{avg_text}</div>
                </div>
            """
        
        # Create three columns for metrics
        col1a, col1b, col1c = st.columns(3)
        
        with col1a:
            st.markdown("**🎯 Daily Goals**")
            st.markdown(custom_metric(
                "Activity Score",
                f"{latest['score']}",
                f"7 Day Avg: {weekly_avg['score']:.0f}"
            ), unsafe_allow_html=True)
            
            st.markdown(custom_metric(
                "Steps",
                f"{latest['steps']:,}/{latest['target_meters']-2000:,}",
                f"7 Day Avg: {weekly_avg['steps']:,.0f}"
            ), unsafe_allow_html=True)
            
        with col1b:
            st.markdown("**🔥 Calories**")
            st.markdown(custom_metric(
                "Active Calories",
                f"{latest['active_calories']:,} kcal",
                f"7 Day Avg: {weekly_avg['active_calories']:,.0f} kcal"
            ), unsafe_allow_html=True)
            
            st.markdown(custom_metric(
                "Total Calories",
                f"{latest['total_calories']:,} kcal",
                f"7 Day Avg: {weekly_avg['total_calories']:,.0f} kcal"
            ), unsafe_allow_html=True)
            
        with col1c:
            st.markdown("**📊 Activity Level**")
            st.markdown(custom_metric(
                "Avg MET",
                f"{latest['average_met_minutes']:.1f}",
                f"7 Day Avg: {weekly_avg['average_met_minutes']:.1f}"
            ), unsafe_allow_html=True)
            
            st.markdown(custom_metric(
                "Distance",
                f"{latest['equivalent_walking_distance']/1000:.1f} km",
                f"7 Day Avg: {weekly_avg['equivalent_walking_distance']/1000:.1f} km"
            ), unsafe_allow_html=True)

    # 2. Daily MET Timeline
    with col1:
        st.subheader("Activity Level Throughout Day")
        latest_activity = activity_df.iloc[-1]
        met_data = [x for x in latest_activity['met_items'] if x is not None]
        
        fig_met = px.line(
            y=met_data,
            x=[i/60 for i in range(len(met_data))],  # Convert to hours
            title="Metabolic Equivalent (MET) Timeline",
            labels={'y': 'MET Score', 'x': 'Hours'}
        )
        
        # Add reference lines for activity levels
        fig_met.add_hline(y=1.7, line_dash="dash", line_color="yellow", annotation_text="Light Activity")
        fig_met.add_hline(y=4, line_dash="dash", line_color="orange", annotation_text="Moderate Activity")
        fig_met.add_hline(y=6, line_dash="dash", line_color="red", annotation_text="Vigorous Activity")
        
        st.plotly_chart(fig_met, use_container_width=True)

    # 3. Activity Metrics Over Time
    with col2:
        st.subheader("Activity Trends Over Time")
        
        # Steps over time
        fig_steps = px.line(
            activity_df,
            y='steps',
            x='date',
            title="Daily Steps",
            labels={'date': 'Date', 'steps': 'Steps'}
        )
        st.plotly_chart(fig_steps, use_container_width=True)
        
        # Calories over time
        fig_calories = px.line(
            activity_df,
            y=['active_calories', 'total_calories'],
            x='date',
            title="Daily Calories",
            labels={'date': 'Date', 'value': 'Calories', 'variable': 'Type'},
            color_discrete_map={
                'active_calories': '#FF6B6B',
                'total_calories': '#4CAF50'
            }
        )
        st.plotly_chart(fig_calories, use_container_width=True)
        
st.title("Activity Tracking 🏃‍♂️")

api_key = st.session_state.get('api_key', None)
if api_key:
    activity_df = process_activity_data(api_key, 30)  # Get 30 days of data
    display_activity_charts(activity_df)
else:
    st.info("Please set up your API key in the Home page.")