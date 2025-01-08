import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def display_sleep_charts(sleep_df):
    # Create three columns
    col1, col2 = st.columns(2)

    # 1. Sleep Metrics
    with col1:
        st.subheader("Sleep Metrics")
        latest = sleep_df.iloc[0]
        
        # Create metrics in a more visual way using st.metric
        col1a, col1b, col1c = st.columns(3)
        
        with col1a:
            st.markdown("**🌙 Sleep Schedule**")
            st.metric("Bedtime", latest['bedtime_start'])
            st.metric("Wake time", latest['bedtime_end'])
            
            st.markdown("**⏱️ Duration**")
            # Convert decimal hours to hours and minutes
            time_in_bed_hrs = int(latest['time_in_bed'])
            time_in_bed_mins = int((latest['time_in_bed'] - time_in_bed_hrs) * 60)
            total_sleep_hrs = int(latest['total_sleep'])
            total_sleep_mins = int((latest['total_sleep'] - total_sleep_hrs) * 60)
            
            st.metric("Time in bed", f"{time_in_bed_hrs}h {time_in_bed_mins}m")
            st.metric("Total sleep", f"{total_sleep_hrs}h {total_sleep_mins}m")
            
        with col1b:
            st.markdown("**📊 Sleep Stages**")
            # Convert sleep stages to hours and minutes
            deep_sleep_hrs = int(latest['deep_sleep'])
            deep_sleep_mins = int((latest['deep_sleep'] - deep_sleep_hrs) * 60)
            light_sleep_hrs = int(latest['light_sleep'])
            light_sleep_mins = int((latest['light_sleep'] - light_sleep_hrs) * 60)
            rem_sleep_hrs = int(latest['rem_sleep'])
            rem_sleep_mins = int((latest['rem_sleep'] - rem_sleep_hrs) * 60)
            
            st.metric("Deep sleep", f"{deep_sleep_hrs}h {deep_sleep_mins}m")
            st.metric("Light sleep", f"{light_sleep_hrs}h {light_sleep_mins}m")
            st.metric("REM sleep", f"{rem_sleep_hrs}h {rem_sleep_mins}m")
        with col1c:
            st.markdown("**❤️ Heart Rate**")
            st.metric("Average", f"{latest['average_hr']:.0f} bpm")
            st.metric("Lowest", f"{latest['lowest_hr']:.0f} bpm")

    # 3. Heart Rate Timeline
    with col1:
        st.subheader("Heart Rate During Sleep")
        latest_sleep = sleep_df.iloc[0]
        hr_data = [x for x in latest_sleep['hr_items'] if x is not None]
        min_hr = min(hr_data)
        min_hr_index = hr_data.index(min_hr)
        
        # Create base line plot
        fig_hr = px.line(
            y=hr_data,
            x= [i*5 for i in range(len(hr_data))],
            title="Heart Rate Throughout Sleep",
            labels={'y': 'Heart Rate (bpm)', 'x': 'Time (5-min intervals)'}
        )
        
        # Add scatter point for lowest HR
        fig_hr.add_trace(
            go.Scatter(
                x=[min_hr_index*5],
                y=[min_hr],
                mode='markers+text',
                marker=dict(color='red', size=10),
                text=[f'Lowest bpm: {min_hr}'],
                textposition='bottom center',
                showlegend=False
            )
        )
        
        st.plotly_chart(fig_hr, use_container_width=True)

    # 4. Sleep Metrics Over Time
    with col2:
        st.subheader("Sleep Metrics Over Time")
        fig_metrics = px.line(
            sleep_df,
            x='date',
            y='total_sleep',
            title="Sleep Duration",
            labels={'y': 'Hours', 'date': 'Date'}
        )
        st.plotly_chart(fig_metrics, use_container_width=True)
        
    # 5. HRV Timeline
    with col2:
        st.subheader("HRV During Sleep")
        hrv_data = [x for x in latest_sleep['hrv_items'] if x is not None]
        fig_hrv = px.line(
            y=hrv_data,
            x= [i*5 for i in range(len(hrv_data))],
            title="HRV Throughout Sleep",
            labels={'y': 'HRV (ms)', 'x': 'Time (5-min intervals)'}
        )
        st.plotly_chart(fig_hrv, use_container_width=True)
