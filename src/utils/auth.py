import streamlit as st

def get_api_key():
    """Get API key based on user selection."""
    data_source = st.radio(
        "Choose data source",
        ["Use demo data", "Connect Oura Ring"]
    )
    
    if data_source == "Connect Oura Ring":
        user_api_key = st.text_input(
            "Enter your Oura API key",
            type="password",
            help="You can find your API key in the Oura web dashboard",
            key="api_key_input"
        )
        
        if user_api_key:
            st.success("API key successfully added! ✅")
            return user_api_key
        return None
    elif data_source == "Use demo data":
        return st.secrets["OURA_API_KEY"]
    return None