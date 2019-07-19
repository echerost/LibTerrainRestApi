import sys
from werkzeug.exceptions import BadRequest
from flask import request,make_response
import LibTerrainRestApi.responseGenerator as resGen
from LibTerrainRestApi.link import Link

def compute_link():
    """
    This function tries to establish a data connection between two points end return link data
    """

    # Get all input data
    myLink : Link = None
    data=None
    # possible error parsing input data
    try:
        data = request.get_json()
        myLink = Link(data)
    except BadRequest:
        print(sys.exc_info()[0])
        return make_response("Unable to parse json payload", 400)
    except IndexError:
        print(sys.exc_info()[0])
        return make_response("Points are not valid", 400)
    except (ValueError, TypeError):
        print(sys.exc_info()[0])
        return make_response("Invalid type: cannot parse link input data", 400)
    except KeyError:
        print(sys.exc_info()[0])
        return make_response("Missing input data: cannot parse link input data", 400)
    except:
        print(sys.exc_info()[0])
        return make_response("Generic error", 500)

    # Create link among two points
    try:
        myLink = myLink.link_two_points()
        returnData = resGen.create_return_data(myLink)
        return resGen.create_json_response(returnData)
    except:
        print(str(sys.exc_info()))
        resp = make_response()
        resp.status_code = 500
        return resp

def get_devices_names():
    """Get the device codes that the user can choose """
    try:
        keys = []
        for device in Link.get_devices():
            keys.append(device)
        response = resGen.create_json_response(keys)          
        return response
    except:
        e = sys.exc_info()
        print(e)
        resp = make_response()
        resp.status_code = 500
        return resp
    
            
