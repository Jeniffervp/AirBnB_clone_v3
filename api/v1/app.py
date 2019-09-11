#!/usr/bin/python3
"""   """
from flask import Blueprint, Flask, jsonify
from models import storage
from api.v1.views import app_views

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
    app.run('0.0.0.0', port=5000, threaded=True)
