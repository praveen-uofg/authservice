import os
from flask import Flask
from app.settings import config
from app.blueprints.ping.api import ping_blueprint
from app.blueprints.authentication.api import authentication_blueprint
from app.blueprints.order.api import order_blueprint
from app.blueprints.product.api import product_blueprint
from app.blueprints.product_order.api import product_order_blueprint
from app.blueprints.error_handler.errors import errors


def setup_app():
    app = Flask(__name__)
    app.register_blueprint(ping_blueprint, url_prefix="/backend/v1/ping")
    app.register_blueprint(errors)
    app.register_blueprint(authentication_blueprint, url_prefix="/backend/v1/auth")
    app.register_blueprint(order_blueprint, url_prefix="/backend/v1/order")
    app.register_blueprint(product_blueprint, url_prefix="/backend/v1/product")
    app.register_blueprint(product_order_blueprint, url_prefix="/backend/v1/orderProduct")

    config_name = os.getenv('ENVIRONMENT')
    if not config_name:
        config_name = "development"
    app.config.from_object(config.app_config[config_name])
    return app
