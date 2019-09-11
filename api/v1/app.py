#!/usr/bin/python3
""" Start the api """
from flask import Blueprint, Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ function to close storage """
    storage.close()


@app.errorhandler(404)
def pagenotfound(e):
    """ handle error 404 """
    return jsonify({"error": "Not found"})

if __name__ == "__main__":
    hs = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    pr = os.environ.get('HBNB_API_PORT', '5000')
    app.run(host=hs, port=pr, threaded=True)
