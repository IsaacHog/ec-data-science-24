from config import LOGGER, HEADERS
from datetime import datetime, timedelta
import time
import requests
import traceback
import json

todays_date = datetime.today()


def throw_error(attempted_action="", error=""):
    LOGGER.error(f"Attempted_action: {attempted_action}")
    LOGGER.error(f"Error: {error}")

def get_events():
    print("Getting events...")
    leagues = [
        "england/premier_league",
        "italy/serie_a",
        "spain/la_liga",
        "germany/bundesliga",
        "france/ligue_1",
    ]
    
    events = []
    for league in leagues:
        url = f'https://eu-offering-api.kambicdn.com/offering/v2018/ubca/listView/football/{league}.json?lang=en_GB&market=ZZ&client_id=2&channel_id=1&ncid=1693053935240&useCombined=true'
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            print()
        else:
            throw_error("Failed to retrieve events", response.status_code)
    print(f"Got {len(events)} events...")
    return events

def bot_loop():
    events = get_events()
    print()

print("--------------- Script initiated--------------------")
try:
    bot_loop()
except Exception:
    throw_error("Last try except", traceback.format_exc())
