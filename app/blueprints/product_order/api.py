from flask import Blueprint, request, abort, make_response, jsonify
from flask_jwt_extended import (jwt_required, current_user)

from app.blueprints.models.model import ProductOrder

product_order_blueprint = Blueprint("product_order_api", __name__)


@product_order_blueprint.route('', methods=['POST'])
@jwt_required
def create():
    if not request.is_json:
        abort(400, description="Missing JSON in request")
    if not current_user:
        abort(401)

    order_id = request.json.get("order_id")
    product_id = request.json.get("product_id")

    if ProductOrder.find_id_by_order_and_product(order_id, product_id):
        abort(409, description="User Role already exists!")

    op = ProductOrder(order_id=order_id, product_id=product_id)
    ProductOrder.save_to_db(op)
    data = {"product_order_id": op.id}
    return make_response(jsonify(data), 200)


