import streamlit as st
from src.utils.data_processing import process_sleep_data
from src.components.sleep_visualizations import display_sleep_charts

st.set_page_config(page_title="Sleep Analysis", page_icon="😴", layout="wide")

st.title("Sleep Analysis 😴")

# Get API key from session state
api_key = st.session_state.get('api_key', None)

if api_key:
    sleep_data = process_sleep_data(api_key)
    display_sleep_charts(sleep_data)