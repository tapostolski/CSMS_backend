from __main__ import app
from database.db_wrapper import DbConnection
from flask import request
from datetime import datetime
import json
from flask_basicauth import BasicAuth

basic_auth = BasicAuth(app)

@app.route('/api/measurement', methods = ['GET'])
@basic_auth.required
def measurements_get_measurements_by_id_GET():
    """get measurements by plant id"""
    start_date = request.args.get('start_date', 0)
    end_date = request.args.get('end_date', datetime.now().timestamp())
    limit = request.args.get('limit', 1000)
    offset = request.args.get('offset', 0)
    every = request.args.get('every', 0)
    # TODO output comment
    db_connection = DbConnection()
    response_json = db_connection.get_measurement(limit = limit, offset = offset, start_date = start_date, end_date = end_date)
    return json.dumps(response_json)

@app.route('/api/measurement/<id>', methods = ['GET'])
@basic_auth.required
def measurements_GET(id):
    """get all measurements"""
    # {"sensor_list": 
    #   [{"sensor_id": sensor id, "plant_id": plant id, "alert_threshold": alert threshold, "last calibration_date": last calibration date}]
    # }
    db_connection = DbConnection()
    response_json = db_connection.get_measurement(id = id)
    return json.dumps(response_json)