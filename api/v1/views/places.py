#!/usr/bin/python3
""" Placex objects that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import Blueprint, Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from pdb import set_trace
import os
import json


@app_views.route("/cities/<city_id>/places", methods=['GET'])
def place_by_state(city_id=None):
    """ return places by city """
    my_dict = []
    ct = {}
    ct = storage.get("City", city_id)
    if ct is None:
        abort(404)
    all_places = storage.all(Place)
    for place in all_places.values():
        if place.city_id == ct.id:
            my_dict.append(place.to_dict())
    return jsonify(my_dict)


@app_views.route("/places/<place_id>", methods=['GET'])
def place(place_id):
    """ getttter an specific place by his id """
    my_dict = []
    pc = {}
    pc = storage.get("Place", place_id)
    if pc is None:
        abort(404)
    return jsonify(pc.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'])
def del_place(place_id):
    """ erase an especific place """
    my_dict = []
    pc = {}
    pc = storage.get("Place", place_id)
    if pc is None:
        abort(404)
    pc.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'])
def post_place(city_id):
    """ actualize the info of a place in a state """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    req = request.get_json()

    if "user_id" not in req:
        return jsonify({"error": "Missing user_id"}), 400

    ur = storage.get("User", req["user_id"])
    if ur is None:
        abort(404)

    if "name" not in req:
        return jsonify({"error": "Missing name"}), 400

    ct = storage.get("City", city_id)
    if ct is None:
        abort(404)

    req.update({"city_id": city_id})
    pc = Place(**req)
    pc.save()
    return jsonify(pc.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'])
def put_place(place_id):
    """ include a new place into a state """
    pc = storage.get("Place", place_id)
    if pc is None:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    req = request.get_json()
    ign = ["id", "city_id", "created_at", "updated_at", "user_id"]
    for k, v in req.items():
        if k not in ign:
            setattr(pc, k, v)
    pc.save()
    return jsonify(pc.to_dict()), 200
