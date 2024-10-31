from flask import Flask
from sqlalchemy.event import api

from app.extensions import db, jwt
from app.config import DevelopmentConfig
from app.routes.category import category
from app.routes.expenses import expense
from app.routes.user import user


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)


    app.register_blueprint(user)
    app.register_blueprint(category)
    app.register_blueprint(expense)

    with app.app_context():
        db.create_all()

    return app