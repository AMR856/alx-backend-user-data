#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask
from flask import Flask, jsonify, abort, request
from flask import url_for, redirect
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth
import logging
app = Flask(__name__)
AUTH = Auth()
logger = logging.getLogger()
logging.basicConfig(filename='hilogger.log')

@app.route('/', methods=['GET'], strict_slashes=False)
def basic_handler() -> str:
    """A basic handler"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_here() -> str:
    """The register is here ain't gonnna lie"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": f"{email}",
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def sessions_handler() -> str:
    """What is that btw?"""
    email = request.form.get('email')
    password = request.form.get('password')
    isValid = AUTH.valid_login(email, password)
    if isValid is False:
        abort(401)
    session_id = AUTH.create_session(email)
    out = jsonify({"email": f"{email}", "message": "logged in"})
    out.set_cookie('session_id', session_id)
    return out


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def session_deleter() -> str:
    """Session deleter can delete the sessions"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user_id=user.id)
    return redirect("/")


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def password_reseter() -> str:
    """Just put some docs here"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200
    except ValueError as error:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile_handler() -> str:
    """Profile handler is here"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": f"{user.email}"})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def password_rest_method() -> str:
    """Update password endpoint"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token=reset_token, password=new_password)
        return jsonify({"email": f"{email}",
                        "message": "Password updated"}), 200
    except ValueError as error:
        abort(403)


if __name__ == "__main__":
    """The main program init"""
    app.run(host="0.0.0.0", port="5000")
