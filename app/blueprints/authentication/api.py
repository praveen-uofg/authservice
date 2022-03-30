import base64

from flask import Blueprint, request, abort, json, make_response, jsonify
from flask_jwt_extended import (create_access_token)
from app.blueprints.models.model import (User)

authentication_blueprint = Blueprint("auth_api", __name__)


@authentication_blueprint.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        abort(400, description="Missing JSON in request")
    data = request.get_json()
    if not all(key in data for key in {"username", "password"}):
        abort(400, description="Missing required parameters")

    username = data['username']
    password = data['password']
    user = User.get_user(username=username)
    if not user:
        abort(404, description="User not found")

    user = next(iter(user))
    if User.check_password(user, password):
        access_token = create_access_token(identity=user.id)
        data = {'access_token': access_token}
        response = {
            'success': True,
            'data': data
        }
        return make_response(jsonify(response), 200)
    abort(401, description="Invalid Phone/Email or Password.")


@authentication_blueprint.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        abort(400, description="Missing JSON in request")
    data = request.get_json()
    if not all(key in data for key in {"first_name", "last_name", "email", "mobile", "password"}):
        abort(400, description="Missing required parameters")

    user = User.get_user(email=data.get("email"), mobile=data.get("mobile"))
    if user:
        abort(409, description="Student already exists!")

    user = User.create_user(data.get("first_name"), data.get("last_name"), data.get("email"), data.get("mobile"),
                            data.get("password"))
    access_token = create_access_token(identity=user.id)
    data = {"access_token": access_token}
    return make_response(jsonify(data), 201)
