import sqlite3
from .db import BaseDbConnection
from datetime import datetime

class Alerts(BaseDbConnection):

    def __init__(self):
        super().__init__()

    def add(self, data, plant_id, measurement_id):
        """adds alert to db"""

        self.cursor.execute(f'INSERT INTO Alerts (measurement_id, plant_id, measurement, date) VALUES ("{measurement_id}", "{plant_id}", "{data["moisture"]}", "{datetime.now().timestamp()}")')
        self.conn.commit()

        return {"alert_id":self.cursor.lastrowid}
    
    def get(self, id = None, plant_id = None,  limit = 35040, offset = 0, start_date = 0, end_date = datetime.now().timestamp(), sort = 'asc'):
        """returns alert if specified by id, if not returns all alerts TODO plantid opis"""
        if id:
            self.cursor.execute(f'SELECT * FROM Alerts WHERE alert_id = {id};')
            response = [self.cursor.fetchone()]
        elif plant_id:
            self.cursor.execute(f'SELECT * FROM Alerts WHERE plant_id = {plant_id} AND date >= {start_date} AND date <= {end_date} LIMIT {offset}, {limit};')
            response = self.cursor.fetchall()
        else:
            print(f'start date: {start_date} end date: {end_date}')
            self.cursor.execute(f'SELECT * FROM Alerts WHERE date >= {start_date} AND date <= {end_date} ORDER BY alert_id {sort} LIMIT {offset}, {limit};')
            response = self.cursor.fetchall()
            
        return_list = []
        for entry in response:
            return_list.append(
                {
                    "alert_id":entry[0],
                    "measurement_id":entry[1],
                    "plant_id":entry[2],
                    "measurement":entry[3],
                    "date":entry[4]
                }
            )
            
        return {"alert_list":return_list}