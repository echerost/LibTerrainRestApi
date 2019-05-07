from datetime import datetime
from flask import request,make_response,jsonify,Response
import libterrain
from shapely.geometry import shape, Point
import geojson
import connexion

DB_CONNECTION_STRING = "postgres://student@192.168.2.48/terrain_ans"
DEFAULT_LOSS_VALUE = 999.9

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
        return create_jsoncreate_json_response(create_empty_return_data(), 500)
    
    # Create link among two points
    link = createLink(shapes, area)

    # Build output data
    retval = None
    if link is None:
        returnData = create_empty_return_data(shapes[0], shapes[1])
        retval = create_json_response(returnData, 200)
    else:
        returnData = create_return_data(shape[0], shape[1],link['loss'], link['src_orient'], link['dst_orient'])
        retval = create_json_response(returnData)

    return retval

def get_shapes_from_geojson(jsonData:dict) -> list :
    """
    This function extracts all geometries from geoJson dict (GeoJson converted in dictionary)

    Keyword argument:
    geoJsonData -- Json following GeoJson specification (https://tools.ietf.org/html/rfc7946) 
    """
    shapes = list()
    #points = jsonData["geoJsonData"]
    src = shape(jsonData["source"])
    dst = shape(jsonData["destination"])
    shapes.append(src)
    shapes.append(dst)
    return shapes

def create_empty_return_data(src:shape, dst:shape) -> dict:
    #src = Point(0.0,0.0)
    retval = create_return_data(src,dst,DEFAULT_LOSS_VALUE,0.0,0.0)
    return retval

def create_return_data(src:shape, dst:shape, loss:float, src_orient:float, dest_orient:float) -> dict:
    is_possible = True
    if loss == DEFAULT_LOSS_VALUE:
        is_possible = False
    retval = {
        'source': geojson.dumps(src),
        'destination': geojson.dumps(dst),
        'link_is_possible': is_possible,
        'loss': loss,
        'source_orientation': src_orient,
        'destination_orientation': dest_orient
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