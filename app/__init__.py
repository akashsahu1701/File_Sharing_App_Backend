import configparser
import logging
from flask import Flask, jsonify
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.logger import RequestFormatter
from app.routes import registered_routes


config = configparser.ConfigParser()
config.read("config.ini")
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config["JWT_SECRET_KEY"] = config.get("settings", "JWT_SECRET_KEY")
    app.config["SECRET_KEY"] = config.get("settings", "SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = config.get(
        "settings", "SQLALCHEMY_DATABASE_URI"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.get(
        "settings", "SQLALCHEMY_TRACK_MODIFICATIONS"
    )

    db.init_app(app)
    JWTManager(app)
    CORS(app)

    registered_routes(app=app)

    # from app.api.users.models import (
    #     User,
    #     Role,
    #     Permission,
    #     UserRole,
    #     RolePermission,
    #     Settings,
    # )

    # from app.api.files.models import File, FilePermission

    # with app.app_context():
    #     db.create_all()

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
