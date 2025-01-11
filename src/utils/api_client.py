import requests

def fetch_daily_data(api_token, endpoint):
    """
    Fetch daily data from the Oura API.
    """
    url = f"https://api.ouraring.com/v2/usercollection/{endpoint}"
    headers = {"Authorization": f"Bearer {api_token}"}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for failed requests
    return response.json()

def fetch_oura_data(api_token, endpoint, num_of_days=7):
    """
    Fetch data from the Oura API.
    Default last 7 days (decluding today)
    """
    
    url = f"https://api.ouraring.com/v2/usercollection/{endpoint}"
    headers = {"Authorization": f"Bearer {api_token}"}
    
    params = get_params(endpoint, num_of_days)
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for failed requests
    return response.json()

def get_params(endpoint, num_of_days):
    """
    Get the start and end dates for a given number of days ago.
    Excludes today to avoid incomplete data.
    Except for certain endpoints such as sleep where today basically means last night.
    """
    from datetime import datetime, timedelta
    
    if endpoint == "sleep":
        today = datetime.now().date()
        x_ago = today - timedelta(days=num_of_days)
        return {
            "start_date": x_ago.strftime("%Y-%m-%d"),
            "end_date": today.strftime("%Y-%m-%d")
        }
    else:
        yesterday = datetime.now().date() - timedelta(days=1)
        x_ago = yesterday - timedelta(days=num_of_days)
        return {
            "start_date": x_ago.strftime("%Y-%m-%d"),
            "end_date": yesterday.strftime("%Y-%m-%d")
        }