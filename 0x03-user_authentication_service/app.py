#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask
from flask import Flask, jsonify, abort, request
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


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


if __name__ == "__main__":
    """The main program init"""
    app.run(host="0.0.0.0", port="5000")
