from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Import config_by_name and specific config classes
from .config import config_by_name, Config, ProductionConfig # Assuming config.py is in the same directory
import os # Import os

db = SQLAlchemy()

# Modify create_app to handle string names and objects
def create_app(config_name_or_object="dev"): # Default to 'dev' name
    app = Flask(__name__)

    is_production = False # Flag to check if using production config

    # Determine the configuration object to use
    if isinstance(config_name_or_object, str):
        # It's a name, look it up in config_by_name
        config_object = config_by_name.get(config_name_or_object)
        if not config_object:
            raise ValueError(f"Invalid configuration name: {config_name_or_object}")
        if config_name_or_object == 'prod':
            is_production = True
    elif isinstance(config_name_or_object, type) and issubclass(config_name_or_object, Config):
        # It's a configuration class/object
        config_object = config_name_or_object
        if config_object == ProductionConfig:
             is_production = True
    else:
        raise TypeError("config_name_or_object must be a string name or a Config class/object")

    # Load configuration from the determined object
    app.config.from_object(config_object)

    # Explicitly handle DATABASE_URL for production *after* loading config
    if is_production:
        db_url = os.environ.get('DATABASE_URL')
        if db_url:
            app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        elif not app.config.get('SQLALCHEMY_DATABASE_URI'): # Check if it wasn't set by the object itself somehow
             # Raise error if DATABASE_URL is mandatory for production and not set
             raise RuntimeError("DATABASE_URL environment variable must be set for production configuration.")

    # Ensure other critical config values are set if not already (removed SQLALCHEMY_DATABASE_URI)
    # app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:') # Removed this line
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    app.config.setdefault('JWT_SECRET_KEY', 'default-jwt-secret-key') # Default for safety

    # Check if URI is set before initializing db
    if not app.config.get('SQLALCHEMY_DATABASE_URI') and not app.config.get('SQLALCHEMY_BINDS'):
         # This check might be redundant now but kept for safety
         raise RuntimeError("Neither 'SQLALCHEMY_DATABASE_URI' nor 'SQLALCHEMY_BINDS' was configured.")

    db.init_app(app)

    # Import and register blueprints after db init
    from .main import bp as main_bp   # blueprint defined in backend/main.py
    app.register_blueprint(main_bp)

    return app