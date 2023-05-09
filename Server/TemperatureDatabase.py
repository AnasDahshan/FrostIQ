import sqlite3
from datetime import datetime

class TemperatureDatabase:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS temperature
                             (id INTEGER PRIMARY KEY AUTOINCREMENT, value REAL, timestamp DATETIME)''')
        self.conn.commit()

    def insert_temperature_with_timestamp(self, timestamp, value):
        self.cursor.execute("INSERT INTO temperature (timestamp, value) VALUES (?, ?)", (timestamp, value))
        self.conn.commit()

    def get_temperatures(self):
        self.cursor.execute("SELECT * FROM temperature")
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
