import logging as logger
from fetch_weather import fetch_weather
from database import init_db, insert_weather, view_db

def setup_logger():
    logger.basicConfig(
    filename="weather.log",
    level=logger.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )

setup_logger()
init_db()

def run():
    data = fetch_weather()
    if data != {}:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        insert_weather(temp=temp, desc=desc)

if __name__ == "__main__":
    run()
    view_db()
