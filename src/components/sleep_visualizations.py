import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def display_sleep_charts(sleep_df):
    # Create three columns
    col1, col2 = st.columns(2)

    # 1. Sleep Metrics
    with col1:
        st.subheader("Sleep Metrics")
        latest = sleep_df.iloc[-1]
        
        # Calculate weekly averages
        weekly_avg = sleep_df.tail(7).mean(numeric_only=True)
        
        # Calculate bedtime/waketime ranges
        bedtimes = pd.to_datetime(sleep_df['bedtime_start'], format='%H:%M').dt.time
        waketimes = pd.to_datetime(sleep_df['bedtime_end'], format='%H:%M').dt.time
        earliest_bed = min(bedtimes).strftime('%H:%M')
        latest_bed = max(bedtimes).strftime('%H:%M') 
        earliest_wake = min(waketimes).strftime('%H:%M')
        latest_wake = max(waketimes).strftime('%H:%M')
        
        # Create metrics in a more visual way using custom HTML/CSS
        col1a, col1b, col1c = st.columns(3)
        
        def custom_metric(label, value, avg_text):
            return f"""
                <div style="margin-bottom: 1rem;">
                    <div style="font-size: 1rem; margin-bottom: 0.2rem;">{label}</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{value}</div>
                    <div style="font-size: 0.8rem; color: #808495;">{avg_text}</div>
                </div>
            """
        
        with col1a:
            st.markdown("**🌙 Sleep Schedule**")
            st.markdown(custom_metric(
                "Bedtime",
                latest['bedtime_start'],
                f"7 Day Range: {earliest_bed} - {latest_bed}"
            ), unsafe_allow_html=True)
            
            st.markdown(custom_metric(
                "Wake time",
                latest['bedtime_end'],
                f"7 Day Range: {earliest_wake} - {latest_wake}"
            ), unsafe_allow_html=True)
            
            time_in_bed_hrs = int(latest['time_in_bed'])
            time_in_bed_mins = int((latest['time_in_bed'] - time_in_bed_hrs) * 60)
            avg_time_in_bed_hrs = int(weekly_avg['time_in_bed'])
            avg_time_in_bed_mins = int((weekly_avg['time_in_bed'] - avg_time_in_bed_hrs) * 60)
            
            st.markdown(custom_metric(
                "Time in bed",
                f"{time_in_bed_hrs}h {time_in_bed_mins}m",
                f"7 Day Avg: {avg_time_in_bed_hrs}h {avg_time_in_bed_mins}m"
            ), unsafe_allow_html=True)
            
        with col1b:
            st.markdown("**📊 Sleep Stages**")
            # Convert sleep stages to hours and minutes for latest
            deep_sleep_hrs = int(latest['deep_sleep'])
            deep_sleep_mins = int((latest['deep_sleep'] - deep_sleep_hrs) * 60)
            light_sleep_hrs = int(latest['light_sleep'])
            light_sleep_mins = int((latest['light_sleep'] - light_sleep_hrs) * 60)
            rem_sleep_hrs = int(latest['rem_sleep'])
            rem_sleep_mins = int((latest['rem_sleep'] - rem_sleep_hrs) * 60)
            
            # Convert sleep stages to hours and minutes for weekly average
            avg_deep_hrs = int(weekly_avg['deep_sleep'])
            avg_deep_mins = int((weekly_avg['deep_sleep'] - avg_deep_hrs) * 60)
            avg_light_hrs = int(weekly_avg['light_sleep'])
            avg_light_mins = int((weekly_avg['light_sleep'] - avg_light_hrs) * 60)
            avg_rem_hrs = int(weekly_avg['rem_sleep'])
            avg_rem_mins = int((weekly_avg['rem_sleep'] - avg_rem_hrs) * 60)
            
            total_sleep_hrs = int(latest['total_sleep'])
            total_sleep_mins = int((latest['total_sleep'] - total_sleep_hrs) * 60)
            avg_total_sleep_hrs = int(weekly_avg['total_sleep'])
            avg_total_sleep_mins = int((weekly_avg['total_sleep'] - avg_total_sleep_hrs) * 60)
            
            st.markdown(custom_metric(
                "Total sleep",
                f"{total_sleep_hrs}h {total_sleep_mins}m",
                f"7 Day Avg: {avg_total_sleep_hrs}h {avg_total_sleep_mins}m"
            ), unsafe_allow_html=True)
            
            st.markdown(custom_metric(
                "Deep sleep",
                f"{deep_sleep_hrs}h {deep_sleep_mins}m",
                f"7 Day Avg: {avg_deep_hrs}h {avg_deep_mins}m"
            ), unsafe_allow_html=True)
            
            st.markdown(custom_metric(
                "Light sleep",
                f"{light_sleep_hrs}h {light_sleep_mins}m",
                f"7 Day Avg: {avg_light_hrs}h {avg_light_mins}m"
            ), unsafe_allow_html=True)
            
            st.markdown(custom_metric(
                "REM sleep",
                f"{rem_sleep_hrs}h {rem_sleep_mins}m",
                f"7 Day Avg: {avg_rem_hrs}h {avg_rem_mins}m"
            ), unsafe_allow_html=True)
            
        with col1c:
            st.markdown("**❤️ Heart Rate**")
            st.markdown(custom_metric(
                "Average",
                f"{latest['average_hr']:.0f} bpm",
                f"7 Day Avg: {weekly_avg['average_hr']:.0f} bpm"
            ), unsafe_allow_html=True)
            
            st.markdown(custom_metric(
                "Lowest",
                f"{latest['lowest_hr']:.0f} bpm", 
                f"7 Day Avg: {weekly_avg['lowest_hr']:.0f} bpm"
            ), unsafe_allow_html=True)

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
        fig_sleep_stages = px.line(
            sleep_df,
            x='date',
            y=['total_sleep', 'deep_sleep', 'light_sleep', 'rem_sleep'],
            title="Sleep Stages Over Time",
            labels={
                'date': 'Date',
                'value': 'Hours',
                'variable': 'Sleep Stage'
            },
            color_discrete_map={
                'total_sleep': '#6E78FF',    # Blue
                'deep_sleep': '#FF6B6B',     # Red
                'light_sleep': '#4CAF50',    # Green
                'rem_sleep': '#FFC107'       # Yellow/Gold
            }
        )
        
        # Update the legend names
        new_names = {
            'total_sleep': 'Total Sleep',
            'deep_sleep': 'Deep Sleep',
            'light_sleep': 'Light Sleep',
            'rem_sleep': 'REM Sleep'
        }
        fig_sleep_stages.for_each_trace(lambda t: t.update(name=new_names[t.name]))
        
        # Update y-axis to show ticks from 0 to 10
        fig_sleep_stages.update_layout(
            yaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=2,
                range=[0, 10]
            )
        )
        
        st.plotly_chart(fig_sleep_stages, use_container_width=True)
        
    # 5. HRV Timeline
    with col1:
        st.subheader("HRV During Sleep")
        hrv_data = [x for x in latest_sleep['hrv_items'] if x is not None]
        fig_hrv = px.line(
            y=hrv_data,
            x= [i*5 for i in range(len(hrv_data))],
            title="Heart Rate Variability Throughout Sleep",
            labels={'y': 'HRV (ms)', 'x': 'Time (5-min intervals)'}
        )
        st.plotly_chart(fig_hrv, use_container_width=True)

    # Add Average Heart Rate Over Time
    with col2:
        st.subheader("Average Heart Rate Over Time")
        fig_avg_hr = px.line(
            sleep_df,
            x='date',
            y='average_hr',
            title="Average Heart Rate During Sleep",
            labels={'y': 'Heart Rate (bpm)', 'date': 'Date'}
        )
        st.plotly_chart(fig_avg_hr, use_container_width=True)

    # Add Lowest Heart Rate Over Time
    with col2:
        st.subheader("Lowest Heart Rate Over Time")
        fig_lowest_hr = px.line(
            sleep_df,
            x='date',
            y='lowest_hr',
            title="Lowest Heart Rate During Sleep",
            labels={'y': 'Heart Rate (bpm)', 'date': 'Date'}
        )
        st.plotly_chart(fig_lowest_hr, use_container_width=True)
