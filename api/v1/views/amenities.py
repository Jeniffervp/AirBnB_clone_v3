#!/usr/bin/python3
""" Amenity objects that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import Blueprint, Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity
from pdb import set_trace
import os
import json


@app_views.route("/amenities")
@app_views.route("/amenities/<amenity_id>", methods=['GET'])
def amenity_id(amenity_id=None):
    """ getttter amenities """
    my_dict = []
    am = {}
    if amenity_id is None:
        am = storage.all("Amenity")
        for i in am.values():
            my_dict.append(i.to_dict())
        return jsonify(my_dict)
    am = storage.get("Amenity", amenity_id)
    if am is None:
        abort(404)
    my_dict.append(am.to_dict())
    return jsonify(my_dict[0])


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def del_amenity(amenity_id):
    """ delete amenities """
    my_dict = []
    am = {}
    am = storage.get("Amenity", amenity_id)
    if am is None:
        abort(404)
    am.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'])
def post_amenity():
    """ update amenity """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    req = request.get_json()
    if "name" not in req:
        return jsonify({"error": "Missing name"}), 400
    am = Amenity(**req)
    am.save()
    return jsonify(am.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def put_amenity(amenity_id):
    """ update amenity """
    am = storage.get("Amenity", amenity_id)
    if am is None:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    req = request.get_json()
    ign = ["id", "amenity_id", "created_at", "updated_at"]
    for k, v in req.items():
        if k not in ign:
            setattr(am, k, v)
    am.save()
    return jsonify(am.to_dict()), 200
