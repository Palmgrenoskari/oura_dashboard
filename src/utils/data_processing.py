import streamlit as st
from src.utils.api_client import fetch_oura_data

API_KEY = st.secrets["OURA_API_KEY"]

def process_sleep_data():
  
  raw_data = fetch_oura_data(API_KEY, "sleep", 7)
  data = raw_data['data']
  
  sleep_data = []
  
  for day in data:
    
    fields_of_interest = {
      "average_breath": day['average_breath'],
      "average_hr": day['average_heart_rate'],
      "average_hrv": day['average_hrv'],
      "awake_time": day['awake_time'],
      "bedtime_end": day['bedtime_end'],
      "bedtime_start": day['bedtime_start'],
      "date": day['day'],
      "hr_items": day['heart_rate']['items'],
      "hrv_items": day['hrv']['items'],
      "time_in_bed": day['time_in_bed'],
      "deep_sleep_duration": day['deep_sleep_duration'],
      "light_sleep_duration": day['light_sleep_duration'],
      "rem_sleep_duration": day['rem_sleep_duration'],
      "total_sleep_duration": day['total_sleep_duration'],
      "lowest_hr": day['lowest_heart_rate'],
      "movement_30_sec": day['movement_30_sec'],
      "efficiency": day['efficiency'],
      "latency": day['latency'],
      "restless_periods": day['restless_periods'],
      "sleep_phase_5_min": day['sleep_phase_5_min'],
    }
    
    sleep_data.append(fields_of_interest)
    
  
  return sleep_data
  
  

def process_activity_data(data):
  return data

def process_readiness_data(data):
  return data