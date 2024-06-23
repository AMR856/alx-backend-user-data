#!/usr/bin/env python3
""" View of session Auth
"""

from flask import jsonify, abort
from models.user import User
from flask import request
from api.v1.views import app_views
from typing import Tuple
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_handler() -> Tuple[str, int]:
    """Do you think I forgot"""
    email = request.form.get('email', None)
    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password', None)
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    my_user_list = User.search({'email': email})
    if len(my_user_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    my_user = my_user_list[0]
    if my_user.is_valid_password(password) is False:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(my_user.id)
    out = jsonify(my_user.to_json())
    session_name = os.getenv('SESSION_NAME', None)
    out.set_cookie(session_name, session_id)
    return out
