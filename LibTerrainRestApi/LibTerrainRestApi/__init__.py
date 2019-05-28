"""
The flask application package.
"""

import connexion
import os
app = connexion.FlaskApp(__name__, specification_dir='./openapi/')
app.add_api('swagger.yaml')
#app.run(host="localhost",port=5000)
import LibTerrainRestApi.views
app.run()