import sqlite3
from .db import BaseDbConnection, generate_update_query_string_from_data


class Sensors(BaseDbConnection):

    def __init__(self):
        super().__init__()

    #CHECK
    def check_if_exists(self, id):
        """returns True if sensor exists in db"""
        self.cursor.execute(f'SELECT 1 FROM Sensors WHERE sensor_id = "{id}";')
        existing_sensor_id = self.cursor.fetchone()
    
        if existing_sensor_id:
            return True 
        else:
            return False
        
    #ADD
    def add_sensor(self, data, timestamp):    
        """adds sensor to db"""                                                                                            # TODO replace placeholder values
        self.cursor.execute(f'INSERT INTO Sensors (sensor_id, alert_threshold, last_calibration_date) VALUES ({data["sensor_id"]}, 35,{timestamp});')
        self.conn.commit()

        return {"sensor_id":self.cursor.lastrowid}
    
    #ADD
    def get_sensors(self, id = None):
        """returns sensor if specified by id, if not returns all sensors"""
        if id:
            self.cursor.execute(f'SELECT * FROM Sensors WHERE sensor_id = "{id}";')
            response = [self.cursor.fetchone()]
        else:
            self.cursor.execute(f'SELECT * FROM Sensors;')
            response = self.cursor.fetchall()
        
        return_list = []
        for entry in response:
            return_list.append(
                {
                    "sensor_id":entry[0],
                    "plant_id":entry[1],
                    "alert_threshold":entry[2],
                    "last_calibration_date":entry[3]
                }
            )
            
        return {"sensor_list":return_list}
    
    def get_alert_threshold(self, id):
        """"""
        self.cursor.execute(f'SELECT alert_threshold FROM Sensors WHERE sensor_id = "{id}";')
        response = self.cursor.fetchone()[0]
        return {"alert_threshold":response}
    
    def edit(self, id, input_data: dict):
        """edits sensor in db"""
        partial_query_string = generate_update_query_string_from_data(input_data)
        self.cursor.execute(f'UPDATE Sensors SET {partial_query_string} WHERE sensor_id = {id};')
        self.conn.commit()

    def delete(self, id):
        """deletes sensor from db"""
        self.cursor.execute(f'DELETE FROM Sensors WHERE sensor_id = {id};')
        self.conn.commit()

