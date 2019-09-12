#!/usr/bin/python3
"""  """
from api.v1.views import app_views
from flask import Blueprint, Flask, jsonify, abort, request
from models import storage
from models.state import State
from pdb import set_trace
import os
import json


def get_id(state_id, stat):
    """  """
    my_dict = []

    for i in stat.values():
        if state_id == i.id:
            my_dict.append(i.to_dict())
    return my_dict


@app_views.route("/states")
@app_views.route("/states/<state_id>", methods=['GET'])
def state_retrieve(state_id=None):
    """  """
    my_dict = []
    if state_id is None:
        st = {}
        st = storage.all("State")
        for i in st.values():
            my_dict.append(i.to_dict())
        return jsonify(my_dict)
    stat = storage.all("State")
    my_dict = get_id(state_id, stat)
    if len(my_dict) == 0:
        abort(404)
    return jsonify(my_dict[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delet_state(state_id=None):
    """  """
    stat = storage.all("State")
    my_dict = []
    for i in stat.values():
        if state_id == i.id:
            my_dict.append(i)
            break
    if len(my_dict) == 0:
        abort(404)
    storage.delete(my_dict[0])
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def body_request():
    """  """
    if not request.is_json:
        print("No a JSON")
        abort(400)
    req = request.get_json()
    if "name" not in req.keys():
        print("Missing name")
        abort(400)
    new_state = State(**req)
    storage.new(new_state)
    storage.save()
    storage.close()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id=None):
    """ """
    if not request.is_json:
        print("No a JSON")
        abort(400)
    req = request.get_json()
    stat = storage.all("State")
    my_dict = []
    for i in stat.values():
        if state_id == i.id:
            my_dict.append(i)
            break
    if len(my_dict) == 0:
        abort(404)
    for j, i in req.items():
        setattr(my_dict[0], j, i)
    storage.save()
    storage.close()
    return jsonify(my_dict[0].to_dict()), 200
