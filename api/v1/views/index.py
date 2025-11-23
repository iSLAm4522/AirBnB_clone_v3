#!/usr/bin/python3
"""Index file for API v1 views."""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"})
