from flask import request,make_response
import libterrain
from shapely.geometry import shape, Point
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
        return responseGenerator.create_jsoncreate_json_response(create_empty_return_data(), 500)
    
    # Create link among two points
    link = createLink(shapes, area)

    # Build output data
    retval = None
    if link is None:
        returnData = responseGenerator.create_empty_return_data(shapes[0], shapes[1])
        retval = responseGenerator.create_json_response(returnData, 200)
    else:
        returnData = responseGenerator.create_return_data(shape[0], shape[1],link['loss'], link['src_orient'], link['dst_orient'])
        retval = responseGenerator.create_json_response(returnData)

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
    BI = libterrain.BuildingInterface.get_best_interface(dbConfig.DB_CONNECTION_STRING, area)
    firstPoint = shapes[0]
    buildingsFirstPoint = BI.get_buildings(shape=firstPoint)
    secondPoint = shapes[1]
    buildingsSecondPoint = BI.get_buildings(shape=secondPoint)

    startCoord = buildingsFirstPoint[0].coord_height()
    endCoord = buildingsSecondPoint[0].coord_height()
    
    # terrain interface initialization
    global STI
    if(STI == None):
       print("STI nulla")
       STI = libterrain.SingleTerrainInterface(dbConfig.DB_CONNECTION_STRING, lidar_table = dbConfig.LIDAR_TABLE_NAME)

    link = None
    if(STI != None):
        try:
            link = STI.get_link(source=startCoord, destination=endCoord)
        except:
            e = sys.exc_info()
            print(e)
    else:
        print("Unable to connect to the database")
    return link