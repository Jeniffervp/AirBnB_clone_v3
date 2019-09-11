#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User


@app_views.route("/status")
def json_status():
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    dicti = {}
    clases = {"amenities": Amenity, "cities": City, "places": Place,
              "reviews": Review, "states": State, "users": User}
    for i, j in clases.items():
        dicti[i] = storage.count(j)
    return jsonify(dicti)
