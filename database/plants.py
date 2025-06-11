import sqlite3
from .db import BaseDbConnection, generate_update_query_string_from_data

class Plants(BaseDbConnection):

    def __init__(self):
        super().__init__()

    def add(self, data):
        """adds plant to db""" 
        self.cursor.execute(f'INSERT INTO Plants (plant_specie, plant_name) VALUES ("{data["plant_specie"]}", "{data["plant_name"]}");')
        
        self.conn.commit()
        return {"plant_id":self.cursor.lastrowid}
    
    def get_id_by_sensor_id(self, sensor_id):
        """"""
        self.cursor.execute(f'SELECT plant_id FROM Sensors WHERE sensor_id = {sensor_id} LIMIT 1;')
        plant_id = self.cursor.fetchone()[0]

        return {"plant_id":plant_id}
    
    def get(self, id = None):
        """returns plant if specified by id, if not returns all plants"""
        if id:
            self.cursor.execute(f'SELECT * FROM Plants WHERE plant_id = "{id}";')
            response = [self.cursor.fetchone()]
        else:
            self.cursor.execute(f'SELECT * FROM Plants;')
            response = self.cursor.fetchall()
        
        return_list = []
        for entry in response:
            return_list.append(
                {
                    "plant_id":entry[0],
                    "plant_specie":entry[1],
                    "plant_name":entry[2]
                }
            )
            
        return {"plant_list":return_list}
    
    def edit(self, id, input_data: dict):
        """edits plant in db"""
        partial_query_string = generate_update_query_string_from_data(input_data)
        self.cursor.execute(f'UPDATE Plants SET {partial_query_string} WHERE plant_id = {id};')
        self.conn.commit()    

    def delete(self, id):
        """deletes plant from db"""
        self.cursor.execute(f'DELETE FROM Plants WHERE plant_id = {id};')
        self.conn.commit()