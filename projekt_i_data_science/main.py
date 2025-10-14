from config import LOGGER, HEADERS, LEAGUES
from datetime import datetime, timedelta
import requests
import traceback
import csv
import os

todays_date = datetime.today()


def throw_error(attempted_action="", error=""):
    LOGGER.error(f"Attempted_action: {attempted_action}")
    LOGGER.error(f"Error: {error}")

def get_events():
    LOGGER.debug("Getting events...")
    events = []
    for league in LEAGUES:
        url = f'https://eu-offering-api.kambicdn.com/offering/v2018/ubca/listView/football/{league}.json?lang=en_GB&market=ZZ&client_id=2&channel_id=1&ncid=1693053935240&useCombined=true'
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            for event in data['events']:
                if datetime.strptime(event['event']['start'], '%Y-%m-%dT%H:%M:%SZ').day != todays_date.day:
                    continue
                if (datetime.strptime(event['event']['start'], '%Y-%m-%dT%H:%M:%SZ') > todays_date + timedelta(minutes=65)):
                    # Hoping to get 2-3 data points per game incase a betoffer is temporarily suspended during one scraping cycle
                    continue

                if event['event']['state'] == 'STARTED':
                    continue
                events.append({
                    'id': event['event']['id'],
                    'match_name': event['event']['englishName'],
                    'event_start': (datetime.strptime(event['event']['start'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=1)).isoformat(),
                })
        else:
            throw_error("Failed to retrieve events", response.status_code)
    LOGGER.debug(f"Got {len(events)} events...")
    return events

def get_events_odds(events):
    def find_odds_in_betoffers(bet_offers):
        def assign_odds(bet_offer_outcomes):
            return [outcome['odds'] for outcome in bet_offer_outcomes]
                
        home_odds = None
        even_odds = None
        away_odds = None
        over_4_5_cards = None
        under_4_5_cards = None # Not logged
        over_2_5_goals = None
        under_2_5_goals = None # Not logged
        for bet_offer in bet_offers:
            if 'Full Time' == bet_offer['criterion']['label']:
                home_odds, even_odds, away_odds = assign_odds(bet_offer['outcomes'])
            elif 'Total Cards' == bet_offer['criterion']['label']:
                if str(bet_offer['outcomes'][0]['line']/1000) != "4.5":
                    continue
                over_4_5_cards, under_4_5_cards = assign_odds(bet_offer['outcomes'])
            elif 'Total Goals' == bet_offer['criterion']['label']: 
                if str(bet_offer['outcomes'][0]['line']/1000) != "2.5":
                    continue
                over_2_5_goals, under_2_5_goals = assign_odds(bet_offer['outcomes'])
            
        return {
            'event_id': event['id'],
            'match_name': event['match_name'],
            'time_stamp': datetime.now().isoformat(timespec='seconds'),
            'event_start': event['event_start'],
            'home_odds': home_odds,
            'even_odds': even_odds,
            'away_odds': away_odds,
            'over_4_5_cards': over_4_5_cards,
            'over_2_5_goals': over_2_5_goals
        }
    
    LOGGER.debug("Getting betoffers...")
    odds = []
    for event in events:
        url = f"https://eu-offering-api.kambicdn.com/offering/v2018/ubca/betoffer/event/{event['id']}.json?lang=en_GB&market=ZZ&client_id=2&channel_id=1&ncid=1698228899164&includeParticipants=true"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            LOGGER.debug(f"Failed to retrieve events for {event['match_name']}:", response.text)
            continue
        data = response.json()
        odds.append(find_odds_in_betoffers(data['betOffers']))
   
    return odds

def log_odds(odds): 
    LOGGER.debug("Logging to csv file...")
    filename = "full_time_log.csv"
    existing_logs = []

    if os.path.exists(filename):
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            existing_logs = list(reader)
    else:
        throw_error("Read full_time_log.csv", "File not found")
        return

    new_entries = []
    for odds in odds:
        new_entries.append(odds)

    combined_logs = existing_logs + new_entries

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["event_id", "match_name", "event_start", "time_stamp", "home_odds", "even_odds", "away_odds", "over_4_5_cards", "over_2_5_goals"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined_logs)
    LOGGER.debug("Logged new entries to csv file")


def main_loop():
    events = get_events()
    odds = get_events_odds(events)
    log_odds(odds)

LOGGER.debug("--------------- Script initiated--------------------")
try:
    main_loop()
except Exception:
    throw_error("Last try except", traceback.format_exc())
