import requests

def fetch_oura_data(api_token, endpoint, num_of_days=7):
    """
    Fetch data from the Oura API.
    Default last 7 days (decluding today)
    """
    
    url = f"https://api.ouraring.com/v2/usercollection/{endpoint}"
    headers = {"Authorization": f"Bearer {api_token}"}
    
    params = get_params(num_of_days)
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for failed requests
    return response.json()

def get_params(num_of_days):
    """
    Get the start and end dates for a given number of days ago.
    """
    
    from datetime import datetime, timedelta
    yesterday = datetime.now().date() - timedelta(days=1)
    
    if num_of_days == 1:
        return {
            "start_date": yesterday.strftime("%Y-%m-%d"),
            "end_date": yesterday.strftime("%Y-%m-%d")
        }
    
    x_ago = yesterday - timedelta(days=num_of_days+1)
    return {
        "start_date": x_ago.strftime("%Y-%m-%d"),
        "end_date": yesterday.strftime("%Y-%m-%d")
    }