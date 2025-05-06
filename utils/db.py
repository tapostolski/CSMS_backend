import sqlite3
from datetime import datetime

class DbConnection:
    #initialize mysql database and/or connection
    def __init__(self):
        self.conn = sqlite3.connect('Measurements.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    #database initial setup 
    def create_table(self):
        
        #returns True if table exists
        def check_if_table_exists(table_name):
            self.cursor.execute(f'SELECT 1 FROM sqlite_master WHERE type="table" AND name = "{table_name}" LIMIT 1;')
            if(self.cursor.fetchone()):
                return True
            else:
                return False

        queries = [
            'CREATE TABLE IF NOT EXISTS Measurements (measurement_id INTEGER PRIMARY KEY AUTOINCREMENT, sensor_id TINYINT, measurement TINYINT, date TIMESTAMP);',
            'CREATE TABLE IF NOT EXISTS Sensors (sensor_id INTEGER PRIMARY KEY, plant_id int, alert_threshold TINYINT, min_raw_value TINYINT, max_raw_value TINYINT, last_calibration_date TIMESTAMP);',
            'CREATE TABLE IF NOT EXISTS Plant_Species (plant_id INTEGER PRIMARY KEY AUTOINCREMENT, plant_specie VARCHAR(50), plant_name VARCHAR(50));'
            # TODO table alerts
        ]

        #loop through queries and check if table exist, if not creates it
        for query in queries:
            table_name = query.split("EXISTS ")[1].split(" (")[0]
            if(not check_if_table_exists(table_name)):
                self.cursor.execute(query) 
                self.conn.commit()

    #TODO comm
    def check_if_sensor_exists(self, data):
        self.cursor.execute(f'SELECT 1 FROM Sensors WHERE sensor_id = "{data["sensor_id"]}";')
        existing_sensor_id = self.cursor.fetchone()
    
        if(existing_sensor_id):
            return True 
        else:
            return False

    #add sensor    
    def add_sensor(self, data, timestamp):
        self.cursor.execute(f'INSERT INTO Sensors (sensor_id, plant_id, alert_threshold, min_raw_value, max_raw_value, last_calibration_date) VALUES ({data["sensor_id"]}, -1, 35, -1, -1,{timestamp});')
        self.conn.commit()

    def add_measurement(self, data, timestamp):
        self.cursor.execute(f'INSERT INTO Measurements (sensor_id, measurement, date) VALUES ({data["sensor_id"]},{data["moisture"]},{timestamp});')
        self.conn.commit()