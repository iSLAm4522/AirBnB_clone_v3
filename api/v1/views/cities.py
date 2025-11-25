#!/usr/bin/python3
"""Views for City objects in the API v1."""
from flask import jsonify, abort, request
from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieve all City objects for a given State ID."""
    if not storage.get(State, state_id):
        abort(404)
    cities = storage.all(City).values()
    lst = []
    for city in cities:
        if city.state_id == state_id:
            lst.append(city.to_dict())
    return jsonify(lst)


@app_views.route('/cities/<city_id>')
def get_city(city_id):
    """Retrieve a City object by ID."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """Delete a City object by ID."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a new City object for a given State ID."""
    if not storage.get(State, state_id):
        abort(404)
    data_dict = request.get_json(silent=True)
    if not request.is_json or not data_dict:
        abort(400, "Not a JSON")
    if data_dict.get('name') is None:
        abort(400, "Missing name")
    data_dict['state_id'] = state_id
    city = City(**data_dict)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Update a City object by ID."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data_dict = request.get_json(silent=True)
    if not request.is_json or not data_dict:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, val in data_dict.items():
        if key not in ignore_keys:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
