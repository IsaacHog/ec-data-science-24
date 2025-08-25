import requests
import logging

def fetch_weather():
    api_key = "4060ecba9fd0a5cd29431bc61f665936"
    lat = 46.4775
    lon = 30.7326
    try:
        #url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return {}

fetch_weather()