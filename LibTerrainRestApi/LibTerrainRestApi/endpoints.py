import sys
from flask import request,make_response
import LibTerrainRestApi.responseGenerator as resGen
from LibTerrainRestApi.link import Link

def compute_link():
    """
    This function tries to establish a data connection between two points end return link data
    """

    # Get all input data
    myLink : Link = None
    # possible error parsing input data
    try:
        data = request.get_json()
        myLink = Link(data)
    except:
        e = sys.exc_info()
        print(e[0])
        return make_response("Invalid input data", 400)

    # Create link among two points
    try:
        myLink = myLink.link_two_points()
        returnData = resGen.create_return_data(myLink)
        return resGen.create_json_response(returnData)
    except:
        # db connection error
        e = sys.exc_info()
        print(e)
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
    
            
