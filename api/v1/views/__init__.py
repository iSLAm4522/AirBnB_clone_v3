#!/usr/bin/python3
"""Init file for API v1 views module."""
from flask import Blueprint

app_views = Blueprint(name='app_views',
                      import_name=__name__,
                      url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
