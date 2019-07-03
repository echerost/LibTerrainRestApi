"""
Routes and views for the flask application.
"""

from flask import render_template
from LibTerrainRestApi.runflask import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'home.html',
        title='Home Page',
    )
