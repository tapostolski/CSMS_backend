from __main__ import app
from flask import request
import json
from database.db_wrapper import DbConnection
from datetime import datetime
from flask_basicauth import BasicAuth

basic_auth = BasicAuth(app)

@app.route('/api/plants', methods = ['POST'])
@basic_auth.required
def plants_add_POST():
    """add plant"""
    # input:
    # {"plant_specie":"specie","plant_name":"name"}
    # output:
    # {"plant_id":plant id}
    data = request.json
    db_connection = DbConnection()
    response_json = db_connection.add_plant(data)
    return json.dumps(response_json)


@app.route('/api/plants', methods = ['GET'])
@basic_auth.required
def plants_get_all_GET():
    """get all plants"""
    # "plant_list": [
    #    {
    #        "plant_id": 1,
    #        "plant_specie": "plant specie",
    #        "plant_name": "plant name"
    #    },]
    db_connection = DbConnection()
    response_json = db_connection.get_plants()
    return json.dumps(response_json)

@app.route('/api/plants/<id>', methods = ['GET'])
@basic_auth.required
def plants_get_by_id_GET(id):
    """get plant by id"""
    #{"plant_id": plant id, "plant_specie": "plant specie", "plant_name": "plant name"}
    db_connection = DbConnection()
    response_json = db_connection.get_plants(id)["plant_list"][0]
    return json.dumps(response_json)
   
@app.route('/api/plants/<id>/measurements', methods = ['GET'])
@basic_auth.required
def plants_get_measurements_by_plant_id_GET(id):
    """get measurements by plant id"""
    start_date = request.args.get('start_date', 0)
    end_date = request.args.get('end_date', datetime.now().timestamp())
    limit = request.args.get('limit', 1000)
    offset = request.args.get('offset', 0)
    sort = request.args.get('sort', 'asc')
    # TODO output comment
    db_connection = DbConnection()
    response_json = db_connection.get_measurements_by_plant_id(id, limit = limit, offset = offset, start_date = start_date, end_date = end_date, sort = sort)
    return json.dumps(response_json)

@app.route('/api/plants/<id>/alerts', methods = ['GET'])
@basic_auth.required
def plants_get_alert_by_plant_id_GET(id):
    """get alert by plant id"""
    start_date = request.args.get('start_date', 0)
    end_date = request.args.get('end_date', datetime.now().timestamp())
    limit = request.args.get('limit', 1000)
    offset = request.args.get('offset', 0)
    #TODO{"plant_id": plant id, "plant_specie": "plant specie", "plant_name": "plant name"}
    db_connection = DbConnection()
    #TODO sprawdzic alert_list binko
    response_json = db_connection.get_alerts(plant_id = id, limit = limit, offset = offset, start_date = start_date, end_date = end_date)
    return json.dumps(response_json)

@app.route('/api/plants/<id>', methods = ['PATCH'])
@basic_auth.required
def plants_PATCH(id):
    """TODO plants change id"""
    # input: { "plant_id":plant id, "alert_threshold":alert threshold }
    db_connection = DbConnection()
    data = request.json
    db_connection.edit_plant(id,data)
    return "", 200

@app.route('/api/plants/<id>', methods = ['DELETE'])
@basic_auth.required
def plants_DELETE(id):
    """TODO plants change id"""
    # input: { "plant_id":plant id, "alert_threshold":alert threshold }
    db_connection = DbConnection()
    db_connection.delete_plant(id)
    return "", 200