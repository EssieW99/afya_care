#!/usr/bin/env python3
"""" the API blueprint"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.user_routes import *
from api.v1.views.claims_routes import *