from flask import Blueprint, request, abort, make_response, jsonify
from flask_jwt_extended import (jwt_required, current_user)

from app.blueprints.models.model import Product
from app.utils.list_utils import to_list

product_blueprint = Blueprint("product_api", __name__)


@product_blueprint.route("", methods=['GET'])
@jwt_required
def index():
    if not request.is_json:
        abort(400, description="Missing JSON in request")
    if not current_user:
        abort(401)
    products = Product.get_products()
    data = {"products": to_list(products)}
    return make_response(jsonify(data), 200)


@product_blueprint.route("/<int:product_id>", methods=['GET'])
@jwt_required
def read(product_id):
    if not request.is_json:
        abort(400, description="Missing JSON in request")
    if not current_user:
        abort(401)

    product = Product.get_product_by_id(product_id)
    if not product:
        abort(404, description="Product doesn't exist")
    data = {"policy": product.to_dict()}
    return make_response(jsonify(data), 200)
