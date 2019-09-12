#!/usr/bin/python3
""" Review objects that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import Blueprint, Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from pdb import set_trace
import os
import json


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def review_by_state(place_id=None):
    """ return reviews by place """
    my_dict = []
    pc = {}
    pc = storage.get("Place", place_id)
    if pc is None:
        abort(404)
    all_reviews = storage.all(Review)
    for review in all_reviews.values():
        if review.place_id == pc.id:
            my_dict.append(review.to_dict())
    return jsonify(my_dict)


@app_views.route("/reviews/<review_id>", methods=['GET'])
def review(review_id):
    """ get an specific review by his id """
    my_dict = []
    rw = {}
    rw = storage.get("Review", review_id)
    if rw is None:
        abort(404)
    return jsonify(rw.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def del_review(review_id):
    """ erase an especific review """
    my_dict = []
    rw = {}
    rw = storage.get("Review", review_id)
    if rw is None:
        abort(404)
    rw.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'])
def post_review(place_id):
    """ actualize the info of a review in a state """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    req = request.get_json()

    pc = storage.get("Place", place_id)
    if pc is None:
        abort(404)

    if "user_id" not in req:
        return jsonify({"error": "Missing user_id"}), 400

    ur = storage.get("User", req["user_id"])
    if ur is None:
        abort(404)

    if "text" not in req:
        return jsonify({"error": "Missing text"}), 400

    req.update({"place_id": place_id})
    rw = Review(**req)
    rw.save()
    return jsonify(rw.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def put_review(review_id):
    """ include a new review into a state """
    rw = storage.get("Review", review_id)
    if rw is None:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    req = request.get_json()
    ign = ["id", "place_id", "created_at", "updated_at", "user_id"]
    for k, v in req.items():
        if k not in ign:
            setattr(rw, k, v)
    rw.save()
    return jsonify(rw.to_dict()), 200
