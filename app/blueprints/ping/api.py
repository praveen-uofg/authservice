from flask import Blueprint, make_response, jsonify

ping_blueprint = Blueprint("ping_api", __name__)


@ping_blueprint.route("/", methods=['GET'])
def get():
    data = {'message': 'Ping processed successfully.'}
    return make_response(jsonify(data), 200)


@ping_blueprint.route("/sentry", methods=['GET'])
def trigger_error():
    division_by_zero = 1 / 0


