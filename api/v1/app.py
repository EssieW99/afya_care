#!/usr/bin/env python3
""" Flask application"""


from api.v1.config import Config
from api.v1.views import app_views
from flask import Flask, jsonify, render_template, make_response
from flask_session import Session
from flask_cors import CORS
import os

app = Flask(__name__, template_folder=Config.TEMPLATE_FOLDER, static_folder=Config.STATIC_FOLDER)
app.config.from_object(Config)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.route('/')
def index():
    """ index page"""

    return render_template('index.html')

@app.route('/login')
def login_sign_in():
    """ login and sign in page"""

    return render_template('login.html')

@app.route('/claim')
def claims():
    """ claim reporting page"""

    return render_template('claims.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
