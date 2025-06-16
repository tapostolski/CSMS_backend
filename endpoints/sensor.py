from __main__ import app
from database.db_wrapper import DbConnection
from flask import request
import json
from flask_basicauth import BasicAuth

basic_auth = BasicAuth(app)

@app.route('/api/sensors', methods = ['GET'])
@basic_auth.required
def sensors_get_all_GET():
    """get all sensors"""
    # {"sensor_list": 
    #   [{"sensor_id": sensor id, "plant_id": plant id, "alert_threshold": alert threshold, "last calibration_date": last calibration date}]
    # }
    db_connection = DbConnection()
    response_json = db_connection.get_sensors()
    print(request.headers)
    return json.dumps(response_json)

@app.route('/api/sensors/<id>', methods = ['GET'])
@basic_auth.required
def sensors_get_by_id_GET(id):
    """sensors get id"""
    # {"sensor_id": sensor id, "plant_id": plant id, "alert_threshold": alert threshold, "last calibration_date": last calibration date}
    db_connection = DbConnection()
    response_json = db_connection.get_sensors(id)["sensor_list"][0]
    return json.dumps(response_json)

@app.route('/api/sensors/<id>', methods = ['PATCH'])
@basic_auth.required
def sensors_PATCH(id):
    """sensors change id"""
    # input: { "plant_id":plant id, "alert_threshold":alert threshold }
    db_connection = DbConnection()
    data = request.json
    db_connection.edit_sensor(id,data)
    return "", 200

@app.route('/api/sensors/<id>', methods = ['DELETE'])
@basic_auth.required
def sensors_DELETE(id):
    """delete sensor by id"""
    db_connection = DbConnection()
    db_connection.delete_sensor(id)
    return "", 200