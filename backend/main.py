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
# Import ov_client from extensions
from .extensions import db, jwt, ov_client, migrate # Added migrate here
# from .extensions import db, jwt # Ensure this uses direct import
# Ensure this line correctly points to your contacts route file:
from .routes.contact_routes import contacts_bp # Should match the actual filename, e.g., contact_routes.py
from .routes.images import images_bp
from .routes.auth import auth_bp # Changed to absolute import
# Revert to direct import
from .models import TokenBlocklist, User # Ensure this uses direct import
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required
)
# Remove OpenverseClient import and initialization from here
# from openverse_client import OpenverseClient
from .config import config_by_name, Config

# --- Initialize Extension Objects (Unbound) ---
cors = CORS() # Initialize CORS object

# --- Create Blueprint ---
bp = Blueprint("main", __name__)

# --- Openverse Client ---
# ov_client = OpenverseClient() # REMOVED: Moved to extensions.py

# --- Import Models AFTER OpenverseClient ---
# This might resolve the circular import if OpenverseClient imports models
# Revert to direct import
from .models import Contact, User, TokenBlocklist # Ensure this uses direct import


# --- Routes ---

# Add the root route to the blueprint
@bp.route("/")
def index():
    """Index route to confirm API is running."""
    # Changed message to match test expectation if needed, or keep as is
    return "API is running" 

# Add the /api route to the blueprint for the test
@bp.route("/api")
def api_index():
    """API index route."""
    return jsonify({"message": "API is running"})

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
        return jsonify({"message": "Login succeeded", "access_token": access_token})
    return jsonify({"message": "Bad username or password"}), 401


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

# Add the @me route BEFORE create_app so it's defined when the blueprint is registered
@bp.route("/@me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Get the currently authenticated user's information."""
    current_user_id = get_jwt_identity()
    # Use session.get() instead of query.get() to avoid LegacyAPIWarning
    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"id": user.id, "username": user.username}), 200

# Add the /api/protected route for the test
@bp.route("/api/protected")
@jwt_required()
def protected_route():
    """A simple protected route."""
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    return jsonify({"message": "This is a protected route", "logged_in_as": user.username})

# --- Application Factory Function ---
def create_app(config_class=Config): # Default to Config class
    """
    Application factory function.
    Configures and returns the Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True) # Use instance folder for config/db

    # Load configuration directly from the provided class object
    app.config.from_object(config_class)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Ensure critical config values are set
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    app.config.setdefault('JWT_SECRET_KEY', 'dev-key-for-testing')
    
    # Import extensions
    from .extensions import db, jwt, cors, migrate, ov_client
    
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db) # Initialize migrate using the imported object
    jwt.init_app(app)
    cors.init_app(app)
    
    # Register JWT token blocklist loader
    @jwt.token_in_blocklist_loader
    def check_if_token_blocklisted(jwt_header, jwt_payload):
        from .models import TokenBlocklist
        jti = jwt_payload["jti"]
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    # Register blueprints after extensions are initialized
    # Register bp at the root URL prefix
    app.register_blueprint(bp, url_prefix='/') 
    app.register_blueprint(contacts_bp, url_prefix='/api/contacts')
    app.register_blueprint(images_bp, url_prefix='/api/images')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    return app

# Entry point for running the Flask application
if __name__ == '__main__':
    # Create the Flask app instance using the factory function
    # Default to 'dev' configuration if FLASK_CONFIG is not set
    config_name = os.environ.get('FLASK_CONFIG', 'dev')
    app_config = config_by_name.get(config_name, Config)
    app = create_app(app_config)
    
    # Run the Flask development server
    # host='0.0.0.0' makes the server accessible externally (e.g., from Docker)
    # debug=True enables automatic reloading and detailed error pages
    # port=5000 specifies the port number
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])