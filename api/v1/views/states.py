#!/usr/bin/python3
"""  """
from flask import Blueprint, Flask, jsonify, abort()
from models import storage
from api.v1.views import app_views
import os
import json

app = Flask(__name__)
app.register_blueprint(app_views)


def get_id(state_id, stat):
    """  """
    my_dict = []

    for i in stat:
        if state_id == i.id:
            for keys, val in i.items():
                my_dict.append({keys: val})
    return my_dict


@app.route('/states', methods=['GET'])
@app.route('/states/<state_id>', methods=['GET'])
def state_retrieve(state_id=None):
    """  """
    if state_id is None:
        return storage.all("State")
    stat = storage.all("State")
    my_dict = get_id(state_id, stat)
    if len(my_dict) == 0:
        abort(404)
    return(my_dict)


@app.route('/states/<state_id>', methods=['DELETE'])
def delet_state(state_id=None):
    """  """
    my_dict = get_id(state_id, stat)
    if len(my_dict) == 0:
        abort(404)
    storage.delete(mydict[0])
    return {}, 200


@app.route('/states/', methods=['POST'])
def body_request():
    """  """
    req = request.json()
    try:
        json.loads(data)
    except ValueError:
        print("Not a JSON")
        abort(404)
    if "name" not in req.keys():
        print("Missing name")
        abort(404)
    return req, 201


@app.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id=None):
    """ """

    req = request.json()
    try:
        json.loads(data)
    except ValueError:
        print("Not a JSON")
        abort(404)
    if "name" not in req.keys():
        print("Missing name")
        abort(404)
    return req, 200

    my_dict = get_id(state_id, stat)
    if len(my_dict) == 0:
        abort(404)
    storage.delete(mydict[0])
    return {}, 200
