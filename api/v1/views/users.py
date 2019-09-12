#!/usr/bin/python3
""" User objects that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import Blueprint, Flask, jsonify, abort, request
from models import storage
from models.user import User
from pdb import set_trace
import os
import json


@app_views.route("/users")
@app_views.route("/users/<user_id>", methods=['GET'])
def user_id(user_id=None):
    """ get users """
    my_dict = []
    us = {}
    if user_id is None:
        us = storage.all("User")
        for i in us.values():
            my_dict.append(i.to_dict())
        return jsonify(my_dict)
    us = storage.get("User", user_id)
    if us is None:
        abort(404)
    my_dict.append(us.to_dict())
    return jsonify(my_dict[0])


@app_views.route("/users/<user_id>", methods=['DELETE'])
def del_user(user_id):
    """ delete users """
    my_dict = []
    us = {}
    us = storage.get("User", user_id)
    if us is None:
        abort(404)
    us.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'])
def post_user():
    """ update user """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    req = request.get_json()
    if "name" not in req:
        return jsonify({"error": "Missing name"}), 400
    us = User(**req)
    us.save()
    return jsonify(us.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'])
def put_user(user_id):
    """ update user """
    us = storage.get("User", user_id)
    if us is None:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    req = request.get_json()
    ign = ["id", "user_id", "created_at", "updated_at"]
    for k, v in req.items():
        if k not in ign:
            setattr(us, k, v)
    us.save()
    return jsonify(us.to_dict()), 200
