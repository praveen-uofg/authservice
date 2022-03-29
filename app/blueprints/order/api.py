from flask import Blueprint, request, abort, make_response, jsonify
from flask_jwt_extended import (jwt_required, current_user)

from app.blueprints.models.model import Order
from app.utils.list_utils import to_list

order_blueprint = Blueprint("order_api", __name__)


@order_blueprint.route('', methods=['GET'])
@jwt_required
def index():
    if not request.is_json:
        abort(400, description="Missing JSON in request")
    if not current_user:
        abort(401)

    requesting_user = current_user['user']
    orders = Order.find_order_by_user_id(requesting_user.get("id"))
    data = {"orders": to_list(orders)}
    return make_response(jsonify(data), 200)


@order_blueprint.route('', methods=['POST'])
@jwt_required
def create():
    if not request.is_json:
        abort(400, description="Missing JSON in request")
    if not current_user:
        abort(401)
    data = request.get_json()
    requesting_user = current_user['user']
    order = Order.create_order(requesting_user.get("id"))
    data = {"order": to_list(order)}
    return make_response(jsonify(data), 200)


@order_blueprint.route('/<int:order_id>', methods=['GET'])
@jwt_required
def read(order_id):
    if not request.is_json:
        abort(400, description="Missing JSON in request")
    if not current_user:
        abort(401)
    requesting_user = current_user['user']
    order = Order.find_order_by_user_id_order_id(requesting_user.get("id"), order_id)
    if not order:
        abort(404, description="Order doesn't exist")
    data = {"order": order.to_dict(), "roles": to_list(order.product_orders)}
    return make_response(jsonify(data), 200)

