from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_object="backend.settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)

    from .main import bp as main_bp   # blueprint defined in backend/main.py
    app.register_blueprint(main_bp)

    return app