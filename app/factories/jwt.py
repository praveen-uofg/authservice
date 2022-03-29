from flask import make_response, jsonify

from app.blueprints.models.model import (User)
from .extensions import jwt


def setup_jwt(app):
    jwt.init_app(app)


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    user = User.query.get(identity)
    if not user:
        return None
    current_user = {
        "user": user,
    }
    return current_user


@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return make_response(jsonify(ret), 404)


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return make_response(jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401)


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    token_type = expired_token['type']
    return make_response(jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401)


@jwt.invalid_token_loader
def invalid_token_callback(error="Invalid Token"):
    return make_response(jsonify(
        {
            "description": "Signature verification failed!",
            "error": "invalid_token"
        }, 401
    ))


@jwt.needs_fresh_token_loader
def fresh_token_loader_callback():
    return jsonify(
        {
            "description": "Token is not fresh. Fresh token needed!",
            "error": "needs_fresh_token"
        }, 401
    )


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.get(identity)
    data = {
        "name": user.first_name + " " + user.last_name,
    }
    return data


@jwt.user_identity_loader
def user_identity_lookup(_id):
    return _id
