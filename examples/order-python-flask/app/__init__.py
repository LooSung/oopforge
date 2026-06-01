from flask import Flask
from flask_smorest import Api

from app.core.config import Config, TestingConfig
from app.order.blueprint import bp as order_bp


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)

    if config_name == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    app.config["API_TITLE"] = "OOPforge Order Service (Flask)"
    app.config["API_VERSION"] = "1.0.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/api/v1"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)
    api.register_blueprint(order_bp)
    return app
