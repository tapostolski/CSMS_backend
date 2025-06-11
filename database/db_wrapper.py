import sqlite3
from .db import BaseDbConnection
from .alerts import Alerts
from .measurements import Measurements
from .plants import Plants
from .sensors import Sensors
from datetime import datetime

#TODO input_data
class DbConnection(BaseDbConnection):

    def __init__(self):
        super().__init__()
    
    def create_table(self):
        """database initial setup"""
        
        def check_if_table_exists(table_name):
            """returns True if table exists"""
            self.cursor.execute(f'SELECT 1 FROM sqlite_master WHERE type="table" AND name = "{table_name}" LIMIT 1;')
            if self.cursor.fetchone():
                return True
            else:
                return False

        #queries initializing tables
        queries = [
            'CREATE TABLE IF NOT EXISTS Plants (plant_id INTEGER PRIMARY KEY AUTOINCREMENT, plant_specie VARCHAR(50), plant_name VARCHAR(50));',
            'CREATE TABLE IF NOT EXISTS Sensors (sensor_id INTEGER PRIMARY KEY, plant_id INT, alert_threshold TINYINT, last_calibration_date TIMESTAMP);',
            'CREATE TABLE IF NOT EXISTS Measurements (measurement_id INTEGER PRIMARY KEY AUTOINCREMENT, sensor_id INT, plant_id INT, measurement TINYINT, date TIMESTAMP);',           
            'CREATE TABLE IF NOT EXISTS Alerts (alert_id INTEGER PRIMARY KEY AUTOINCREMENT, measurement_id INT, plant_id INT, measurement TINYINT, date TIMESTAMP)'
        ]

        #loop through queries and check if table exist, if not creates it
        for query in queries:
            table_name = query.split("EXISTS ")[1].split(" (")[0]
            if not check_if_table_exists(table_name):
                self.cursor.execute(query) 
                self.conn.commit()

    #CHECK
    def check_if_sensor_exists(self, data):
        """returns True if sensor exists in db"""

        return Sensors().check_if_exists(data["sensor_id"])
        
   #ADD
    def add_sensor(self, data, timestamp):    
        """adds sensor to db""" 

        return Sensors().add_sensor(data, timestamp)
 
    def add_measurement(self, data, timestamp):
        """adds measurement to db""" 

        return Measurements().add(data, timestamp)

    def add_plant(self, data):
        """adds plant to db""" 

        return Plants().add(data)
    
    def add_alert(self, data, plant_id, measurement_id):
        """adds alert to db"""

        return Alerts().add(data, plant_id,measurement_id)

    #GET
    def get_measurements_by_plant_id(self, plant_id, limit = 100, offset = 0, start_date = 0, end_date = datetime.now().timestamp(), sort = 'asc'):
        """gets measurement from plant id, default with limit 100 and offset 0
        
        TODO 
        """ 

        return Measurements().get_by_plant_id(plant_id, limit, offset, start_date, end_date, sort)
    
    def get_plant_id_by_sensor_id(self, sensor_id):
        """"""

        return Plants().get_id_by_sensor_id(sensor_id)
    
    def get_plants(self, id = None):
        """returns plant if specified by id, if not returns all plants"""
        
        return Plants().get(id)
        

    def get_measurement(self, id = None, limit = 35040, offset = 0, start_date = 0, end_date = datetime.now().timestamp()):
        """"""

        return Measurements().get(id, limit, offset, start_date, end_date)

    def get_sensors(self, id = None):
        """returns sensor if specified by id, if not returns all sensors"""
        return Sensors().get_sensors(id = id)
    
    def get_alert_threshold(self, id):
        """"""
        
        return Sensors().get_alert_threshold(id)
    
    # 35040 measurements in year (1 measurement per 15 min)
    def get_alerts(self, id = None, plant_id = None,  limit = 35040, offset = 0, start_date = 0, end_date = datetime.now().timestamp()):
        """returns alert if specified by id, if not returns all alerts TODO plantid opis"""
        
        return Alerts().get(id, plant_id, limit, offset, start_date, end_date)

    #EDDIT
    def edit_sensor(self, id, input_data: dict):
        """edits sensor in db"""
        return Sensors().edit(id, input_data)

    def edit_plant(self, id, input_data: dict):
        """edits plant in db"""
        return Plants().edit(id, input_data)

    #DELETE
    def delete_plant(self, id):
        """deletes plant from db"""
        return Plants().delete(id)

#TODO generate jakistam string from data