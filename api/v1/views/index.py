#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route("/status")
def json_status():
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats():
    clases = ["Amenity", "City", "Place", "Review", "State", "User"]
    dicti = {}
    for i in clases:
        dicti.setdefault(i, storage.count(i))
    return jsonify(dicti)
