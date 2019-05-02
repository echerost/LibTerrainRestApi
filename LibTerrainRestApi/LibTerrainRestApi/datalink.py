from datetime import datetime
from flask import request,make_response,jsonify
import geojson
import json
from shapely.geometry import shape, mapping
import connexion

def get_timestamp():
   return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def compute_link():
    """
    This function tries to establish a data connection between two points end return link data
    """
    jsonData = request.get_json()
    # Get GeoJson geometries and convert them to shapely format
    features = jsonData["features"]
    shapes = list()
    try:
        shapes=get_shapes_from_geojson(jsonData)
    except:
        return makemake_response(400)
    return jsonify("All ok")#TODO: ritornare dati elaborati

def get_shapes_from_geojson(jsonData:dict) -> list :
    shapes = list()
    for feature in jsonData["features"]:
        geom = shape(feature["geometry"])
        shapes.append(geom)
    return shapes
