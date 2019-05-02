"""
This script runs the LibTerrainRestApi application using a development server.
"""

import connexion
app = connexion.FlaskApp(__name__, specification_dir='LibTerrainRestApi/openapi/')
app.add_api('swagger.yaml')
#app.run(host="localhost",port=5000)
app.run()
import LibTerrainRestApi.views

#from os import environ
#from LibTerrainRestApi import app
#if __name__ == '__main__':
#    HOST = environ.get('SERVER_HOST', 'localhost')
#    try:
#        PORT = int(environ.get('SERVER_PORT', '5555'))
#    except ValueError:
#        PORT = 5555
#    app.run(HOST, PORT)
