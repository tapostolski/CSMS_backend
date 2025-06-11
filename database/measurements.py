from datetime import datetime
from .db import BaseDbConnection

class Measurements(BaseDbConnection):

    def __init__(self):
        super().__init__()
    
    
    def get(self, id = None, limit = 35040, offset = 0, start_date = 0, end_date = datetime.now().timestamp()):
        """returns measurement if specified by id, if not returns all measurements"""
        if id:
            self.cursor.execute(f'SELECT * FROM Measurements WHERE measurement_id = "{id}";')
            response = [self.cursor.fetchone()]
        else:
            self.cursor.execute(f'SELECT * FROM Measurements WHERE date >= {start_date} AND date <= {end_date} LIMIT {offset}, {limit};')
            response = self.cursor.fetchall()
            
        return_list = []
        for entry in response:
            return_list.append(
                {
                    "measurement_id":entry[0],
                    "sensor_id":entry[1],
                    "plant_id":entry[2],
                    "measurement":entry[3],
                    "date":entry[4],
                }
            )
            
        return {"measurement_list":return_list}

    def add(self, data, timestamp):
        """adds measurement to db""" 
        self.cursor.execute(f'SELECT plant_id FROM Sensors WHERE sensor_id={data["sensor_id"]};')
        plant_id = self.cursor.fetchone()[0]
        if plant_id != None:
            self.cursor.execute(f'INSERT INTO Measurements (sensor_id, plant_id, measurement, date) VALUES ({data["sensor_id"]}, {plant_id}, {data["moisture"]}, {timestamp});')
            self.conn.commit()

        return {"measurement_id":self.cursor.lastrowid}
    
    def get_by_plant_id(self, plant_id, limit = 100, offset = 0, start_date = 0, end_date = datetime.now().timestamp(), sort = 'asc'):
        """gets measurement from plant id, default with limit 100 and offset 0
        
        TODO 
        """ 
        self.cursor.execute(f'SELECT * FROM Measurements WHERE plant_id = {plant_id} AND date >= {start_date} AND date <= {end_date} ORDER BY measurement_id {sort} LIMIT {offset}, {limit};')
        response = self.cursor.fetchall()

        return_list = []
        for entry in response:
            return_list.append(
                {
                    "measurement_id":entry[0],
                    "sensor_id":entry[1],
                    "plant_id":entry[2],
                    "measurement":entry[3],
                    "date":entry[4]
                }
            )

        return {"measurement_list":return_list}