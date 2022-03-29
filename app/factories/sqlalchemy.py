from app.blueprints.models.model import db


def setup_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all(app=app)

    return db

