import requests

def fetch_oura_data(api_token, endpoint, days=7):
    """
    Fetch data from the Oura API.
    """
    url = f"https://api.ouraring.com/v2/usercollection/{endpoint}"
    headers = {"Authorization": f"Bearer {api_token}"}
    
    params = get_params(days)
    
    if params is None:
        response = requests.get(url, headers=headers)
    else:  
        response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for failed requests
    return response.json()

def get_params(days):
    """
    Get the start and end dates for a given number of days ago.
    """
    # If we want to get data for today, we don't need to pass in params
    if days == 1:
        return None
    
    from datetime import datetime, timedelta
    today = datetime.now().date()
    x_ago = today - timedelta(days=days)
    return {
        "start_date": x_ago.strftime("%Y-%m-%d"),
        "end_date": today.strftime("%Y-%m-%d")
    }