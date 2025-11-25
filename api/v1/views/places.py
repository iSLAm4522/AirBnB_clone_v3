#!/usr/bin/python3
"""views for Place objects in the API v1."""
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieve all Place objects for a given City ID."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object by ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """Delete a Place object by ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new Place object for a given City ID."""
    if not storage.get(City, city_id):
        abort(404)
    data_dict = request.get_json(silent=True)
    if not request.is_json or not data_dict:
        abort(400, "Not a JSON")
    if not data_dict.get('name'):
        abort(400, "Missing name")
    if not data_dict.get('user_id'):
        abort(400, "Missing user_id")
    if not storage.get(User, data_dict['user_id']):
        abort(404)
    place = Place(**data_dict)
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update a Place object by ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data_dict = request.get_json(silent=True)
    if not request.is_json or not data_dict:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data_dict.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
