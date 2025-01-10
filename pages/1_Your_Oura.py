import streamlit as st
from src.utils.api_client import fetch_oura_data

api_key = st.session_state.get('api_key', None)

st.set_page_config(page_title="Your Oura", page_icon="💍", layout="wide")

st.title("Your Oura 💍")

# Get API key from session state
api_key = st.session_state.get('api_key', None)

if api_key:
    oura_data = fetch_oura_data(api_key, "ring_configuration", 2)
    if oura_data['data'] == []:
      st.info("Action is currently not supported.")
    else:
      st.write(oura_data['data'])

