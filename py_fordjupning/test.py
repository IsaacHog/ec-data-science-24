import pytest
from fetch_weather import fetch_weather

def test_fetch_weather_valid(lat, lon):
    data = fetch_weather(lat, lon)
    assert "main" in data
    assert "weather" in data

def test_fetch_weather_invalid(lat, lon):
    data = fetch_weather(lat, lon)
    assert data == {}

test_fetch_weather_valid(lat = 46.775, lon = 30.7326)
test_fetch_weather_invalid(lat = 46.775, lon = 30000.7326)

