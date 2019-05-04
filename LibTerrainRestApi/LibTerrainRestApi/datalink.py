from datetime import datetime
from flask import request,make_response,jsonify,Response
import libterrain
from shapely.geometry import shape, Point
import geojson
import connexion

DB_CONNECTION_STRING = "postgres://student@192.168.2.48/terrain_ans"

def compute_link():
    """
    This function tries to establish a data connection between two points end return link data
    """
    jsonInputData = request.get_json()

    # Get GeoJson geometries and convert them to shapely format
    area = jsonInputData["area"]
    shapes = list()
    try:
        shapes = get_shapes_from_geojson(jsonInputData)
    except:
        return make_response(400)
    
    # Create link among two points
    link = createLink(shapes, area)

    # Build output data
    retval = None
    if link is None:
        returnData = create_empty_return_data()
        retval = create_json_response(returnData, 400)
    else:
        returnData = create_return_data(shape[0], shape[1], 32.4)
        retval = create_json_response(returnData)

    return retval

def get_shapes_from_geojson(jsonData:dict) -> list :
    """
    This function extracts all geometries from geoJson dict (GeoJson converted in dictionary)

    Keyword argument:
    geoJsonData -- Json following GeoJson specification (https://tools.ietf.org/html/rfc7946) 
    """
    shapes = list()
    featuresCollection = jsonData["geoJsonData"]
    for feature in featuresCollection["features"]:
        geom = shape(feature["geometry"])
        shapes.append(geom)
    return shapes

def create_empty_return_data() -> dict:
    src = Point(0.0,0.0)
    retval = create_return_data(src,src,0.0)
    return retval

def create_return_data(src:shape, dst:shape, maxSpeed:float) -> dict:
    retval = {
        'source': geojson.dumps(src),
        'destination': geojson.dumps(dst),
        'maxSpeed': maxSpeed
        }
    return retval

def create_json_response(responseData:dict, statusCode:int=200) -> Response:
        retval = jsonify(responseData)
        retval.status_code = statusCode
        return retval

def createLink(shapes: list, area: str) -> dict:
    # Recover from DB the two buildings between trying to establish the link
    BI = libterrain.BuildingInterface.get_best_interface(DB_CONNECTION_STRING, area)
    firstPoint = shapes[0]
    buildingsFirstPoint = BI.get_buildings(shape=firstPoint)
    secondPoint = shapes[1]
    buildingsSecondPoint = BI.get_buildings(shape=secondPoint)

    STI = libterrain.SingleTerrainInterface(DB_CONNECTION_STRING, lidar_table="lidar")
    startCoord = buildingsFirstPoint[0].coord_height()
    endCoord = buildingsSecondPoint[0].coord_height()
    link = STI.get_link(source=startCoord, destination=endCoord)
    return link