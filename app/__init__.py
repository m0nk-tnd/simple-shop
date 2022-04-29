from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate

from config import Config

from .products import controllers as product_controllers
from .products import models as product_models
from .orders import controllers as orders_controllers
from .orders import models as order_models
from .database import db

api = Api()


def create_app() -> Flask:
    """create, init and return Flask app"""
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    db.init_app(flask_app)
    migrate = Migrate(flask_app, db)

    api.init_app(flask_app)
    api.add_namespace(product_controllers.api)
    api.add_namespace(orders_controllers.api)

    # @api.errorhandler(ValidationError)
    # def handle_unexpected_within_restx(e):
    #     data = e.messages
    #     # https://github.com/noirbizarre/flask-restplus/issues/530
    #     e.data = data
    #     return {}, 400
    #
    # @api.errorhandler(JWTExtendedException)
    # def handle_jwt_errors(e):
    #     return {"message": str(e)}, 401
    #
    # @jwt.user_lookup_loader
    # def user_lookup_callback(_jwt_header, jwt_data) -> Optional[User]:
    #     identity = jwt_data["sub"]
    #     return get_user_by_identity(identity)

    return flask_app


flask_app = create_app()
