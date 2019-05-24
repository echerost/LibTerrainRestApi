from flask import jsonify,Response
import geojson
from shapely.geometry import shape

DEFAULT_LOSS_VALUE = 999.9

def create_empty_return_data(src:shape, dst:shape) -> dict:
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
