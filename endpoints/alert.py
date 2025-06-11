from __main__ import app
from flask import request
import json
from database.db_wrapper import DbConnection
from datetime import datetime
from flask_basicauth import BasicAuth

basic_auth = BasicAuth(app)

@app.route('/api/alerts', methods = ['GET'])
@basic_auth.required
def alerts_get_all_GET():
    """"""
    # TODO {"sensor_list": 
    #   [{"sensor_id": sensor id, "plant_id": plant id, "alert_threshold": alert threshold, "last calibration_date": last calibration date}]
    # }
    start_date = request.args.get('start_date', 0)
    end_date = request.args.get('end_date', datetime.now().timestamp())
    limit = request.args.get('limit', 35040)
    offset = request.args.get('offset', 0)

    db_connection = DbConnection()
    response_json = db_connection.get_alerts(limit = limit, offset = offset, start_date = start_date, end_date = end_date)
    
    return json.dumps(response_json)

@app.route('/api/alerts/<id>', methods = ['GET'])
@basic_auth.required
def alerts_get_by_id_GET(id):
    """get alert by id"""
    #TODO{"plant_id": plant id, "plant_specie": "plant specie", "plant_name": "plant name"}
    db_connection = DbConnection()
    response_json = db_connection.get_alerts(id = id)["alert_list"][0]
    return json.dumps(response_json)