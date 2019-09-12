#!/usr/bin/python3
""" Start the api """
from flask import Blueprint, Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(err):
    """ function to close storage """
    storage.close()


@app.errorhandler(404)
def pagenotfound(e):
    """ handle error 404 """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', '5000')
    app.run(host=host, port=int(port), threaded=True)
