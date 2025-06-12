from flask import Flask, request
import sqlite3
from datetime import datetime
from database.db_wrapper import DbConnection
import json
from flask_cors import CORS
from flask_basicauth import BasicAuth
from flask import make_response
import base64
import argparse

#initialize flask app
app = Flask("SMM backend")
CORS(app)
import endpoints

#make sure all tables are present
global_db_connection = DbConnection()
global_db_connection.create_table()

loginArgParser = argparse.ArgumentParser(description='Sensor App Login Credentials')
loginArgParser.add_argument('--username', type=str, required=True, help='Username for basic auth')
loginArgParser.add_argument('--password', type=str, required=True, help='Password for basic auth')
loginArgs = loginArgParser.parse_args()

app.config['BASIC_AUTH_USERNAME'] = loginArgs.username
app.config['BASIC_AUTH_PASSWORD'] = loginArgs.password
#app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

#authentication endpoints
@app.route('/api/login', methods=['GET'])
def login_GET():
    """handle GET request for login"""
    header = request.headers
    if 'Authorization' in header:
        auth_type, credentials = header['Authorization'].split(' ', 1)
        if auth_type.lower() == 'basic':
            #username, password = credentials.encode('utf-8').decode('b64').split(':', 1)
            username, password = base64.b64decode(credentials).decode('utf-8').split(':', 1)
            if username == app.config['BASIC_AUTH_USERNAME'] and password == app.config['BASIC_AUTH_PASSWORD']:
                return {"message": "Login successful"}, 200

@app.route('/api/login', methods=['OPTIONS'])
def login_OPTIONS():
    """handle OPTIONS request for login"""
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

#sensors endpoint handling POST
@app.route('/sensor', methods = ['POST'])
@basic_auth.required
def sensor_handle_POST():
    """handle POST from sensor"""
    data = request.json
    timestamp = str(datetime.now().timestamp())
    
    db_connection = DbConnection()

    sensor_exists = db_connection.check_if_sensor_exists(data)

    #if sensor doesn't exist create one
    if not sensor_exists:
        db_connection.add_sensor(data, timestamp)
        print(f'Inserting sensor: {data["sensor_id"]}')
        
    measurement_id = db_connection.add_measurement(data, timestamp)["measurement_id"]

    if data["moisture"] <= db_connection.get_alert_threshold(data["sensor_id"])["alert_threshold"]:
        plant_id = db_connection.get_plant_id_by_sensor_id(data["sensor_id"])["plant_id"]
        db_connection.add_alert(data, plant_id, measurement_id)

    return {"response": measurement_id}

app.run("0.0.0.0", 80)