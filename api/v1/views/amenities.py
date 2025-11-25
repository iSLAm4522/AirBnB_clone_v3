#!/usr/bin/python3
"""Views for Amenity objects in the API v1."""
from flask import jsonify, abort, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """Retrieve all Amenity objects."""
    amenities = storage.all(Amenity).values()
    lst = [obj.to_dict() for obj in amenities]
    return jsonify(lst)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve an Amenity object by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Delete an Amenity object by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Create a new Amenity object."""
    data_dict = request.get_json(silent=True)
    if not request.is_json or not data_dict:
        abort(400, "Not a JSON")
    if not data_dict.get('name'):
        abort(400, "Missing name")
    amenity = Amenity(**data_dict)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update an Amenity object by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data_dict = request.get_json(silent=True)
    if not request.is_json or not data_dict:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, val in data_dict.items():
        if key not in ignore_keys:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
