import streamlit as st
from src.utils.api_client import fetch_oura_data
from datetime import datetime
import pandas as pd

API_KEY = st.secrets["OURA_API_KEY"]

def process_sleep_data(api_key):
  
  raw_data = fetch_oura_data(API_KEY, "sleep", 7)
  data = raw_data['data']
  
  sleep_data = []
  
  for day in data:
    
    # Convert timestamps to datetime objects
    bedtime_start = datetime.fromisoformat(day['bedtime_start'])
    bedtime_end = datetime.fromisoformat(day['bedtime_end'])
    
    # Convert durations from seconds to hours
    fields_of_interest = {
      "date": day['day'],
      "deep_sleep": round(day['deep_sleep_duration'] / 3600, 2),
      "light_sleep": round(day['light_sleep_duration'] / 3600, 2),
      "rem_sleep": round(day['rem_sleep_duration'] / 3600, 2),
      "total_sleep": round(day['total_sleep_duration'] / 3600, 2),
      "time_in_bed": round(day['time_in_bed'] / 3600, 2),
      "sleep_efficiency": day['efficiency'],
      "average_hr": day['average_heart_rate'],
      "average_hrv": day['average_hrv'],
      "lowest_hr": day['lowest_heart_rate'],
      "hr_items": day['heart_rate']['items'],
      "hrv_items": day['hrv']['items'],
      "bedtime_start": bedtime_start.strftime('%H:%M'),
      "bedtime_end": bedtime_end.strftime('%H:%M'),
    }
    
    sleep_data.append(fields_of_interest)
    
  # Convert to pandas DataFrame for easier visualization
  return pd.DataFrame(sleep_data)
  
def process_activity_data(data):
  return data

def process_readiness_data(data):
  return data