#!/usr/bin/python3
"""API v1 application entry point."""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Teardown method to close the storage session."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with a JSON response."""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    """Run the Flask application."""
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', 5000)),
            threaded=True)
