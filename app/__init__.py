import configparser
import logging
from flask import Flask, jsonify
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.logger import RequestFormatter
from app.routes import registered_routes


config = configparser.ConfigParser()
config.read("config.ini")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config["JWT_SECRET_KEY"] = config.get("settings", "JWT_SECRET_KEY")
    app.config["SECRET_KEY"] = config.get("settings", "SECRET_KEY")
    JWTManager(app)
    CORS(app)

    registered_routes(app=app)

    # Configure logging
    handler = logging.StreamHandler()
    handler.setFormatter(
        RequestFormatter(
            "%(asctime)s %(remote_addr)s %(url)s %(levelname)s %(message)s"
        )
    )

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({"message": "Welcome to file sharing Backend!"})

    return app
