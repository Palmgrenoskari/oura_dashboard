import requests

def fetch_oura_data(api_token, endpoint):
    """
    Fetch data from the Oura API.

    Args:
        api_token (str): Oura API token.
        endpoint (str): Endpoint to fetch data from ('sleep', 'activity', 'readiness').

    Returns:
        dict: Response data as JSON.
    """
    url = f"https://api.ouraring.com/v2/usercollection/{endpoint}"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for failed requests
    return response.json()
