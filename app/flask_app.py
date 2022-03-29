from flask_cors import CORS
from app.factories.application import setup_app
from app.factories.logging import setup_logging
from app.factories.sqlalchemy import setup_db
from app.factories.jwt import setup_jwt

flask_app = setup_app()
CORS(flask_app, expose_headers="*")
db = setup_db(flask_app)
setup_jwt(flask_app)
setup_logging()


if __name__ == '__main__':
    flask_app.run()
