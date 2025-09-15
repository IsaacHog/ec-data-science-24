from config import LOGGER, HEADERS, LEAGUES
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
    events = []
    for league in LEAGUES:
        url = f'https://eu-offering-api.kambicdn.com/offering/v2018/ubca/listView/football/{league}.json?lang=en_GB&market=ZZ&client_id=2&channel_id=1&ncid=1693053935240&useCombined=true'
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            for event in data['events']:
                if datetime.strptime(event['event']['start'], '%Y-%m-%dT%H:%M:%SZ').day != todays_date.day:
                    continue
                if event['event']['state'] == 'STARTED':
                    continue
                events.append({
                    'id': event['event']['id'],
                    'match_name': event['event']['englishName'],
                    'eventStart': (datetime.strptime(event['event']['start'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=1)).isoformat(),
                })
        else:
            throw_error("Failed to retrieve events", response.status_code)
    print(f"Got {len(events)} events...")
    return events

def get_betoffers(events):
    print("Getting betoffers...")
    betoffers = []
    for event in events:
        url = f"https://eu-offering-api.kambicdn.com/offering/v2018/ubca/betoffer/event/{event['id']}.json?lang=en_GB&market=ZZ&client_id=2&channel_id=1&ncid=1698228899164&includeParticipants=true"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to retrieve events for {event['match_name']}:", response.text)
            continue
        
        data = response.json()
        print()


def bot_loop():
    events = get_events()
    betoffers = get_betoffers(events)
    print()

print("--------------- Script initiated--------------------")
try:
    bot_loop()
except Exception:
    throw_error("Last try except", traceback.format_exc())
