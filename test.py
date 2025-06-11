from flask import Flask, request

#TODO doc strings  """plants get id"""

#initialize flask app
app = Flask("sensors_app")
#GET
@app.route('/api/plants', methods = ['GET'])
def plants_get_all_GET():
    """get all plants"""
    # "plant_list": [
    #    {
    #        "plant_id": 1,
    #        "plant_specie": "plant specie",
    #        "plant_name": "plant name"
    #    },]
    return "git"

app.run('0.0.0.0', 34197)

