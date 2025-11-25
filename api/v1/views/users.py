#!/usr/bin/python3
"""views for User objects in the API v1."""
from flask import jsonify, abort, request
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """Retrieve all User objects."""
    users = storage.all(User).values()
    lst = [obj.to_dict() for obj in users]
    return jsonify(lst)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieve a User object by ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """Delete a User object by ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Create a new User object."""
    data_dict = request.get_json(silent=True)
    if not request.is_json or not data_dict:
        abort(400, "Not a JSON")
    if not data_dict.get('email'):
        abort(400, "Missing email")
    if not data_dict.get('password'):
        abort(400, "Missing password")
    user = User(**data_dict)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Update a User object by ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data_dict = request.get_json(silent=True)
    if not request.is_json or not data_dict:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data_dict.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
