#!/usr/bin/python3
""" City objects that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import Blueprint, Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.state import City
from pdb import set_trace
import os
import json


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def city_by_state(state_id=None):
    """ return cities by state """
    my_dict = []
    st = {}
    st = storage.get("State", state_id)
    if st is None:
        abort(404)
    for i in st.cities:
        my_dict.append(i.to_dict())
    return jsonify(my_dict)


@app_views.route("/cities/<city_id>", methods=['GET'])
def city(city_id):
    """ get an specific city by his id """
    my_dict = []
    st = {}
    st = storage.get("City", city_id)
    if st is None:
        abort(404)
    return jsonify(st.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def del_city(city_id):
    """ erase an especific city """
    my_dict = []
    st = {}
    st = storage.get("City", city_id)
    if st is None:
        abort(404)
    st.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def post_city(state_id):
    """ actualize the info of a city in a state """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    req = request.get_json()

    if "name" not in req:
        return jsonify({"error": "Missing name"}), 400

    st = storage.get("State", state_id)

    if st is None:
        abort(404)

    req.update({"state_id": state_id})
    st = City(**req)
    st.save()
    return jsonify(st.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'])
def put_city(city_id):
    """ include a new city into a state """
    ct = storage.get("City", city_id)
    if ct is None:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    req = request.get_json()
    ign = ["id", "state_id", "created_at", "updated_at"]
    for k, v in req.items():
        if k not in ign:
            setattr(ct, k, v)
    ct.save()
    return jsonify(ct.to_dict()), 200
