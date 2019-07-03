from flask import jsonify,Response
from geojson import dumps, LineString,Feature, FeatureCollection
from LibTerrainRestApi.link import Link

def create_return_data(link:Link) -> dict:
    if(link is None): raise TypeError('link is None')
    retval = {
        link.SRC_POINT: dumps(link.src),
        link.DST_POINT: dumps(link.dst),
        link.LINK_POSSIBLE: link.is_possible
        }
    if link.is_possible:
        retval[link.LOSS] = link.loss,
        retval[link.SRC_ORIENTATION] = link.src_orientation,
        retval[link.DST_ORIENTATION] = link.dst_orientation,
        # list of profile points    
        feature = Feature(geometry=LineString(link.profile))
        feat_collection = FeatureCollection([feature])
        retval[link.PROFILE] = feat_collection
        offsets={
               link.SRC_OFFSET:link.src_offset,
               link.DST_OFFSET:link.dst_offset
                }
        retval[link.OFFSETS]= offsets
        retval[link.BITRATE]=link.bitrate
    return retval

def create_json_response(responseData, statusCode:int=200) -> Response:
    retval = jsonify(responseData)
    retval.status_code = statusCode
    return retval
                                                                                                                  