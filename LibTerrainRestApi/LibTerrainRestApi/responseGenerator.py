from flask import jsonify,Response
from geojson import dumps, LineString,Feature, FeatureCollection
from shapely.geometry import shape
from LibTerrainRestApi.classes.link import Link


#def create_empty_return_data(src:shape, dst:shape) -> dict:
#    retval = create_return_data(src,dst,DEFAULT_LOSS_VALUE,0.0,0.0)
#    return retval
def create_return_data(link:Link) -> dict:
    if(link is None): raise TypeError('link is None')
    retval = {
        'source': dumps(link.source),
        'destination': dumps(link.destination),
        'link_is_possible': link.is_possible
        }
    if link.is_possible:
         retval['loss'] = link.loss,
         retval['source_orientation'] = link.source_orientation,
         retval['destination_orientation'] = link.destination_orientation,
         feature = Feature(geometry=LineString(link.profile))
         feat_collection = FeatureCollection([feature])
         retval['profile'] = feat_collection
         offsets={
                'source':link.source_offset,
                'destination':link.destination_offset
                }
         retval['offsets']= offsets
    return retval

def create_json_response(responseData:dict, statusCode:int=200) -> Response:
        retval = jsonify(responseData)
        retval.status_code = statusCode
        return retval
                                                                                                                  