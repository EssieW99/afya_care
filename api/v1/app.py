#!/usr/bin/env python3
""" Flask application"""


from api.v1.views import app_views
from flask import Flask, jsonify, render_template, make_response
from flask_session import Session
from flask_cors import CORS
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.register_blueprint(app_views)
app.secret_key = 'deathly_hallows'
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.route('/')
def index():
    """ index page"""

    return render_template('index.html')

@app.route('/login')
def login_sign_in():
    """ login and sign in page"""

    return render_template('login.html')

@app.route('/personal_info')
def personal_info():
    """ personal information page"""

    return render_template('personal_info.html')

@app.route('/claim')
def claims():
    """ claim reporting page"""

    return render_template('claims.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
