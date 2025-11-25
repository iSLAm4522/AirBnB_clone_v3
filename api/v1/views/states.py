#!/usr/bin/python3
"""Views for State objects in the API v1."""
from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Retrieve all State objects."""
    objs = storage.all(State).values()
    lst = []
    for obj in objs:
        lst.append(obj.to_dict())
    return jsonify(lst)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state(state_id):
    """Retrieve a State object by ID."""
    obj = storage.get(State, state_id)
    if obj is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """Delete a State object by ID."""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new State object."""
    data_dict = request.get_json(silent=True)
    if not request.is_json or data_dict is None:
        abort(400, "Not a JSON")
    if data_dict.get('name') is None:
        abort(400, "Missing name")
    state = State(**data_dict)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State object by ID."""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data_dict = request.get_json(silent=True)
    if not request.is_json or data_dict is None:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data_dict.items():
        if key not in ignore_keys:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
