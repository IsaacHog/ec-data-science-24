import sqlite3
import logging

def init_db():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            temperature REAL,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_weather(temp, desc):
    try:
        conn = sqlite3.connect("weather.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO weather (temperature, description)
            VALUES (?, ?)
        """, (temp, desc))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error inserting data: {e}")

def view_db():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM weather")
    rows = cursor.fetchall()

    print("weather.db:")
    for row in rows:
        print(row)

    conn.close()
