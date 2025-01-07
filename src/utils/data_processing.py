import streamlit as st
from src.utils.api_client import fetch_oura_data

API_KEY = st.secrets["OURA_API_KEY"]

def process_sleep_data():
  
  data = fetch_oura_data(API_KEY, "sleep", 7)
  return data

def process_activity_data(data):
  return data

def process_readiness_data(data):
  return data