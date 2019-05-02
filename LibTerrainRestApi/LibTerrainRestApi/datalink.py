from datetime import datetime
from flask import request,make_response
import json
from shapely.geometry import shape
import connexion

def get_timestamp():
   return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

LINK = {
      "TSpeed":{
         "max": "18.0",
         "min":"2.41",
         "timestamp": get_timestamp()
         },
      "RSpeed":{
         "max": "15.1",
         "min": "1.82",
         "timestamp": get_timestamp()
         }
}

def compute_link():
    """
    This function tries to establish a data connection between two points end return link data
    """
    data=request.get_json()
    #data = points
    #geom = shape(data)
    #max=18.0
    #min=2.41
    #time=get_timestamp()
    #retval=jsonify(points=data, maxSpeed=max, minSpeed=min, timestamp=time)
    #retval=make_response(points=data, maxSpeed=max, minSpeed=min, timestamp=time)
    return make_response("cacca")
