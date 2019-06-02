import sys
from flask import request,make_response,jsonify,Response
import libterrain
from shapely.geometry import shape, Point,mapping
import connexion
import LibTerrainRestApi.responseGenerator as resGen
import config.db_config as dbConfig
import psycopg2.errors

STI = None

def compute_link():
    """
    This function tries to establish a data connection between two points end return link data
    """
    jsonInputData = request.get_json()

    # Get GeoJson geometries and convert them to shapely format
    shapes = list()
    try:
        shapes = get_shapes_from_geojson(jsonInputData)
        # Create link among two points
        link = createLink(shapes)
        # if link is None no link is possible
        if link:
            returnData = resGen.create_return_data(shapes[0], shapes[1],link['loss'], link['src_orient'], link['dst_orient'])
            return resGen.create_json_response(returnData)
        else:
            returnData = resGen.create_empty_return_data(shapes[0], shapes[1])
            return resGen.create_json_response(returnData)
         
    except psycopg2.errors.InternalError as e:
        e = sys.exc_info()
        #point = Point(0.0,0.0)
        #returnData = responseGenerator.create_empty_return_data(point,point)
        #return responseGenerator.create_json_response(returnData, 400)
        return make_response("Invalid input", 400)
    except:
        e=sys.exc_info()[1]
        return make_response(e, 500)

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

def createLink(shapes: list) -> dict:

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
       #print("STI nulla")
       STI = libterrain.SingleTerrainInterface(dbConfig.DB_CONNECTION_STRING, lidar_table = dbConfig.LIDAR_TABLE_NAME)
    link = STI.get_link(source=start, destination=end)
    return link