import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def display_activity_charts(activity_df, selected_day, start_date, end_date):
    # Create two columns
    col1, col2 = st.columns(2)

    # 1. Activity Metrics
    # TODO: Rethink the layout of this section
    with col1:
        st.subheader("Activity Metrics")
        selected_day_activity = activity_df[activity_df['date'] == selected_day.strftime('%Y-%m-%d')].iloc[0]
        date_range_activity_df = activity_df[(activity_df['date'] >= start_date.strftime('%Y-%m-%d')) & (activity_df['date'] <= end_date.strftime('%Y-%m-%d'))]

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
                f"{selected_day_activity['score']}",
                f"7 Day Avg: {weekly_avg['score']:.0f}"
            ), unsafe_allow_html=True)
            
            st.markdown(custom_metric(
                "Steps",
                f"{selected_day_activity['steps']:,}/{selected_day_activity['target_meters']-2000:,}",
                f"7 Day Avg: {weekly_avg['steps']:,.0f}"
            ), unsafe_allow_html=True)
            
        with col1b:
            st.markdown("**🔥 Calories**")
            st.markdown(custom_metric(
                "Active Calories",
                f"{selected_day_activity['active_calories']:,} kcal",
                f"7 Day Avg: {weekly_avg['active_calories']:,.0f} kcal"
            ), unsafe_allow_html=True)
            
            st.markdown(custom_metric(
                "Total Calories",
                f"{selected_day_activity['total_calories']:,} kcal",
                f"7 Day Avg: {weekly_avg['total_calories']:,.0f} kcal"
            ), unsafe_allow_html=True)
            
        with col1c:
            st.markdown("**📊 Activity Level**")
            st.markdown(custom_metric(
                "Avg MET",
                f"{selected_day_activity['average_met_minutes']:.1f}",
                f"7 Day Avg: {weekly_avg['average_met_minutes']:.1f}"
            ), unsafe_allow_html=True)
            
            st.markdown(custom_metric(
                "Distance",
                f"{selected_day_activity['equivalent_walking_distance']/1000:.1f} km",
                f"7 Day Avg: {weekly_avg['equivalent_walking_distance']/1000:.1f} km"
            ), unsafe_allow_html=True)

    # 2. Daily MET Timeline
    with col1:
        st.subheader("Activity Level Throughout Day")
        
        # TODO: Better x-axis, need to convert UTC to local
        met_data = [x for x in selected_day_activity['met_items'] if x is not None]
        
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
        
        
        # Add new section for calories visualization
        # TODO: Figure out the correct title/header size and make graph more pleasant to look at
        st.subheader("Daily & Cumulative Active Calories")
        
        # Create figure with bar and line chart using plotly express
        fig = px.bar(
            date_range_activity_df,
            x=date_range_activity_df.index,
            y='active_calories',
            title="Daily & Cumulative Active Calories",
            labels={'active_calories': 'Daily Active Calories'},
            color_discrete_sequence=['#4CAF50']
        )

        # Add cumulative line using plotly express
        fig.add_scatter(
            x=date_range_activity_df.index,
            y=date_range_activity_df['active_calories'].cumsum(),
            name='Cumulative Active Calories',
            yaxis='y2',
            line=dict(color='#2E6B94', width=2)
        )

        # Update layout
        fig.update_layout(
            yaxis2=dict(title='Cumulative Active Calories', overlaying='y', side='right'),
            hovermode='x unified',
            height=400,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)
        
        # Steps over time
        fig_steps = px.line(
            date_range_activity_df,
            y='steps',
            x='date',
            title="Daily Steps",
            labels={'date': 'Date', 'steps': 'Steps'}
        )
        st.plotly_chart(fig_steps, use_container_width=True)
        
        # Calories over time
        fig_calories = px.line(
            date_range_activity_df,
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