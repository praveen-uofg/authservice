import logging
from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)
logger = logging.getLogger('azent')


@errors.app_errorhandler(Exception)
def handle_unexpected_error(e):
    logger.exception(e)

    status_code = 500
    success = False
    response = {
        'success': success,
        'error': {
            'type': 'UnexpectedException',
            'message': 'An unexpected error has occurred.'
        }
    }
    return jsonify(response), status_code
