# File: backend/main.py

import os
import sys
import datetime # Moved import higher as it's used in logout

from flask import Flask, Blueprint, request, jsonify
# Remove unused SQLAlchemy import here if db comes from extensions
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
# Revert to direct import
from backend.extensions import db, jwt 
# from .extensions import db, jwt # Ensure this uses direct import
# Ensure this line correctly points to your contacts route file:
from backend.routes.contact_routes import contacts_bp # Should match the actual filename, e.g., contact_routes.py
from backend.routes.images import images_bp
from backend.routes.auth import auth_bp # Changed to absolute import
# Revert to direct import
from backend.models import TokenBlocklist, User # Ensure this uses direct import
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required
)
# Import OpenverseClient first
from openverse_client import OpenverseClient

# --- Initialize Extension Objects (Unbound) ---
cors = CORS() # Initialize CORS object

# --- Create Blueprint ---
bp = Blueprint("main", __name__)

# --- Openverse Client ---
ov_client = OpenverseClient()  # Can initialize here if it doesn't need app config

# --- Import Models AFTER OpenverseClient ---
# This might resolve the circular import if OpenverseClient imports models
# Revert to direct import
from backend.models import Contact, User, TokenBlocklist # Ensure this uses direct import


# --- Routes ---
@bp.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409
    new_user = User(username=username)
    new_user.set_password(password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error registering user: {str(e)}")
        return jsonify({"message": "Registration failed due to server error"}), 500
    access_token = create_access_token(identity=str(new_user.id))
    return jsonify({"message": "User registered successfully!", "access_token": access_token}), 201

# Add login route if missing
@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401


@bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Logout route to add token JTI to the blocklist."""
    jti = get_jwt()["jti"]
    now = datetime.datetime.utcnow() # Get current time
    # Add token JTI to the database blocklist
    revoked_token = TokenBlocklist(jti=jti, created_at=now)
    try:
        db.session.add(revoked_token)
        db.session.commit()
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error revoking token: {str(e)}") # Log the error
        return jsonify({"message": "Logout failed due to server error"}), 500


# --- Application Factory Function ---
def create_app(config_object='config.Config'): # Point to a Config class within config.py
    """Flask application factory."""
    app = Flask(__name__)

    # Load configuration from config module/object
    try:
        # Attempt to load from the specified object (e.g., config.Config)
        app.config.from_object(config_object)
    except ImportError:
        print(f"Warning: Config object '{config_object}' not found or contains import errors. Loading from environment variables or defaults.")
        # Fallback: Load essential config from environment or set defaults
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_secret_key'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///app.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'jwt_secret_key'),
            # Add other necessary default configs
        )
    except Exception as e:
         print(f"Error loading configuration: {e}. Using defaults.")
         # Apply defaults if any other error occurs during config loading
         app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_secret_key'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///app.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'jwt_secret_key'),
         )


    # Initialize extensions WITH the app instance
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app) # Initialize CORS with the app
    Migrate(app, db) # Initialize Migrate here, after db and app are available

    # Register JWT callbacks
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        # Import model locally to avoid potential early import issues
        # Revert to direct import
        from backend.models import TokenBlocklist # Ensure this uses direct import
        jti = jwt_payload["jti"]
        # Query the database for the token JTI
        token_in_db = TokenBlocklist.query.filter_by(jti=jti).first()
        return token_in_db is not None # Return True if token exists (is blocklisted)

    # Register the Blueprint
    app.register_blueprint(bp)  # Register blueprint at root path '/'

    # Register blueprints
    app.register_blueprint(contacts_bp, url_prefix='/api/contacts')
    app.register_blueprint(images_bp, url_prefix='/api/images') # Ensure images_bp is registered
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Removed database creation from app factory
    # Consider using Flask-Migrate commands ('flask db init', 'flask db migrate', 'flask db upgrade')
    # or handle table creation explicitly in test fixtures.
    # with app.app_context():
    #     db.create_all()

    return app

# Ensure datetime is imported if used (e.g., in logout)
# import datetime # Already imported above