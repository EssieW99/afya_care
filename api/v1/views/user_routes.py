""" API routes for the user model"""

from api.v1.views import app_views
from models.auth import Auth
from models.db import DB
from models.user import User
from flask import Flask, flash, jsonify, request, make_response, abort, redirect, session, render_template, url_for


AUTH = Auth()
db = DB()

@app_views.route('/admin/dashboard', methods=['GET'], strict_slashes=False)
def admin_dashboard():
    """
    route that leads to the admin dashboard
    """

    return render_template('admin_dashboard.html')

@app_views.route('/user/dashboard', methods=['GET'], strict_slashes=False)
def user_dashboard():
    """
    route that leads the user to the user admin dashboard
    """

    return render_template('user_dashboard.html')

@app_views.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """
    an endpoint that registers a new user
    """

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing data"}), 400

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    national_id = data.get('national_id')
    phone_number = data.get('phone_number')
    password = data.get('password')
    try:

        user = AUTH.register_user(first_name=first_name, last_name=last_name, email=email,
                           national_id=national_id, phone_number=phone_number, password=password)
        session['user_id'] = user.id
        session['user_email'] = user.email

        if db.is_email_for_admin(user.email):
            session['user_role'] = 'admin'
            return jsonify({'message': 'SignIn successful!', 'redirect_url': url_for('app_views.admin_dashboard')}), 200
        session['user_role'] = 'user'
        return jsonify({'message': 'SignIn successful!', 'redirect_url': url_for('app_views.user_dashboard')}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@app_views.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """
    creates a new session for the user
    """

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing data"}), 400

    email = data.get('email')
    password = data.get('password')    

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    user = AUTH.valid_login(email=email, password=password)

    if user:
        session['user_id'] = user.id
        session['user_email'] = user.email

        if db.is_email_for_admin(user.email):
            session['user_role'] = 'admin'
            print("Admin login detected. Redirecting to admin dashboard.")
            return jsonify({'message': 'Login successful!', 'redirect_url': url_for('app_views.admin_dashboard')}), 200
        session['user_role'] = 'user'
        print("User login detected. Redirecting to user dashboard.")
        return jsonify({'message': 'Login successful!', 'redirect_url': url_for('app_views.user_dashboard')}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app_views.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    logs out a user
    """

    user_id = session.get('user_id')
    if user_id:
        session.pop('user_id', None)
        flash('Log Out Successful!')
        return redirect('/')
    else:
        flash('Not logged in')
        return redirect('/')


@app_views.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    used to find the user
    """

    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app_views.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    generates a password reset token for a user
    """

    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app_views.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    updates the new set password to the database
    """

    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


