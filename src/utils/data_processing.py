import streamlit as st
from src.utils.api_client import fetch_oura_data, fetch_daily_data
from datetime import datetime
import pandas as pd

def process_sleep_data(api_key, day_count):
  """
  Process sleep data from the Oura API.
  """
  
  raw_data = fetch_oura_data(api_key, "sleep", day_count)
  data = raw_data['data']
  
  sleep_data = []
  
  for day in data:
    # Convert timestamps to datetime objects
    bedtime_start = datetime.fromisoformat(day['bedtime_start'])
    bedtime_end = datetime.fromisoformat(day['bedtime_end'])
    
    # Generate timestamps for each 5-minute interval
    # This helps us later when plotting hr and hrv data against time
    # Filter out None values from heart rate items
    hr_items = [x for x in day['heart_rate']['items'] if x is not None]
    hrv_items = [x for x in day['hrv']['items'] if x is not None]
    hr_count = len(hr_items)
    timestamps = []
    current_time = bedtime_start
    
    for _ in range(hr_count):
        timestamps.append(current_time.strftime('%H:%M'))
        current_time = current_time + pd.Timedelta(minutes=5)
    
    # Calculate total sleep duration in hours
    total_sleep_hours = day['total_sleep_duration'] / 3600
    
    # Skip if sleep duration is less than 3 hours (likely a nap)
    if total_sleep_hours < 3:
      continue
    
    # Convert durations from seconds to hours
    fields_of_interest = {
      "date": day['day'],
      "deep_sleep": round(day['deep_sleep_duration'] / 3600, 2),
      "light_sleep": round(day['light_sleep_duration'] / 3600, 2),
      "rem_sleep": round(day['rem_sleep_duration'] / 3600, 2),
      "total_sleep": round(total_sleep_hours, 2),
      "time_in_bed": round(day['time_in_bed'] / 3600, 2),
      "sleep_efficiency": day['efficiency'],
      "average_hr": day['average_heart_rate'],
      "average_hrv": day['average_hrv'],
      "lowest_hr": day['lowest_heart_rate'],
      "hr_items": hr_items,
      "hrv_items": hrv_items,
      "timestamp_items": timestamps,
      "bedtime_start": bedtime_start.strftime('%H:%M'),
      "bedtime_end": bedtime_end.strftime('%H:%M'),
    }
    
    sleep_data.append(fields_of_interest)
    
  # Convert to pandas DataFrame for easier visualization
  return pd.DataFrame(sleep_data)
  
def process_activity_data(api_key, days):
  """
  Process activity data from the Oura API.
  
  Looks like using the start_date and end_date params in the fetch_oura_data function
  always results in the current day being excluded.
  
  So we're going to do an extra fetch using fetch_daily_data to get today's data.
  """
  
  raw_data = fetch_oura_data(api_key, "daily_activity", days)
  data = raw_data['data']
  
  todays_data = fetch_daily_data(api_key, "daily_activity")
  data.append(todays_data['data'][0])
  
  activity_data = []
  
  for day in data:
    fields_of_interest = {
      "date": day['day'],
      "score": day['score'],
      "active_calories": day['active_calories'],
      "average_met_minutes": day['average_met_minutes'],
      "equivalent_walking_distance": day['equivalent_walking_distance'],
      "met_items": day['met']['items'],
      "steps": day['steps'],
      "target_meters": day['target_meters'],
      "target_calories": day['target_calories'],
      "total_calories": day['total_calories'],
    }
    
    activity_data.append(fields_of_interest)
    
  return pd.DataFrame(activity_data)  

def process_readiness_data(data):
  return data

def load_activity_data():
  return pd.read_parquet('src/data/activity_data.parquet')

def load_sleep_data():
  return pd.read_parquet('src/data/sleep_data.parquet')
