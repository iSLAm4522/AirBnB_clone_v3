#!/usr/bin/python3
"""Views for PlaceReview objects in the API v1."""
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieve all Review objects for a given Place ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review object by ID."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """Delete a Review object by ID."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a new Review object for a given Place ID."""
    if not storage.get(Place, place_id):
        abort(404)
    data_dict = request.get_json(silent=True)
    if not request.is_json or not data_dict:
        abort(400, "Not a JSON")
    if not data_dict.get('user_id'):
        abort(400, "Missing user_id")
    if not storage.get(User, data_dict['user_id']):
        abort(404)
    if not data_dict.get('text'):
        abort(400, "Missing text")
    review = Review(**data_dict)
    review.place_id = place_id
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a Review object by ID."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data_dict = request.get_json(silent=True)
    if not request.is_json or not data_dict:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data_dict.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
