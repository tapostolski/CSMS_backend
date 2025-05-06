from flask import Flask, request
import sqlite3
from datetime import datetime
from utils.db import DbConnection

#initialize flask app
app = Flask("sensors_app")



#handling of POST 
@app.route('/', methods = ['POST', 'GET'])
def handle_request():
    data = request.json
    timestamp = str(datetime.now().timestamp())
    db_connection = DbConnection()

    db_connection.create_table()

    #if sensor doesn't exist create one
    if(not db_connection.check_if_sensor_exists(data)):
        db_connection.add_sensor(data, timestamp)
        print(f'Inserting sensor: {data["sensor_id"]}')
    
    #print(datetime.utcfromtimestamp(float(timestamp)).date())
    
    db_connection.add_measurement(data, timestamp)
    return {"response": "jest git"}
app.run("0.0.0.0", 6969)

