import sys
from flask import request,make_response,jsonify,Response
import libterrain
from shapely.geometry import shape, Point,mapping
import connexion
import LibTerrainRestApi.responseGenerator as responseGenerator
import config.db_config as dbConfig

STI = None


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
        point = Point(0.0,0.0)
        returnData = responseGenerator.create_empty_return_data(point,point)
        return responseGenerator.create_json_response(returnData, 400)
    
    # Create link among two points
    link = createLink(shapes, area)

    # Build output data
    retval = None
    if link:
        returnData = responseGenerator.create_return_data(shapes[0], shapes[1],link['loss'], link['src_orient'], link['dst_orient'])
        retval = responseGenerator.create_json_response(returnData)
    else:
        returnData = responseGenerator.create_empty_return_data(shapes[0], shapes[1])
        retval = responseGenerator.create_json_response(returnData, 200)       

    return retval

def get_shapes_from_geojson(jsonData:dict) -> list :
    """
    This function extracts all geometries from geoJson dict (GeoJson converted in dictionary)

    Keyword argument:
    geoJsonData -- Json following GeoJson specification (https://tools.ietf.org/html/rfc7946) 
    """
    shapes = list()
    src = shape(jsonData["source"])
    dst = shape(jsonData["destination"])
    shapes.append(src)
    shapes.append(dst)
    return shapes

def createLink(shapes: list, area: str) -> dict:
    # Recover from DB the two buildings between trying to establish the link

    #import LibTerrainRestApi.config as config
    #BI =
    #libterrain.BuildingInterface.get_best_interface(config.DB_CONNECTION_STRING,
    #area)
    #import config.config as config
    #BI =
    #libterrain.BuildingInterface.get_best_interface(dbConfig.DB_CONNECTION_STRING,
    #area)
    #firstPoint = shapes[0]
    #buildingsFirstPoint = BI.get_buildings(shape=firstPoint)
    #secondPoint = shapes[1]
    #buildingsSecondPoint = BI.get_buildings(shape=secondPoint)

    #startCoord = buildingsFirstPoint[0].coord_height()
    #endCoord = buildingsSecondPoint[0].coord_height()

    start = {
        'coords': shapes[0],
         'height': 4,
         'optionals': 'start'
        }
    end = {
        'coords': shapes[1],
        'height': 4,
        'optionals': 'end'
        }
    
    # terrain interface initialization
    global STI
    if(STI == None):
       print("STI nulla")
       STI = libterrain.SingleTerrainInterface(dbConfig.DB_CONNECTION_STRING, lidar_table = dbConfig.LIDAR_TABLE_NAME)

    link = None
    try:
       #link = STI.get_link(source=start, destination=end)
       link = STI.get_link(source=start, destination=end)
    except:
       e = sys.exc_info()
       print(e)
    else:
        print("Unable to connect to the database")
    return link