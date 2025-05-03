# File: backend/main.py

# --- Core Imports ---
import os
import sys
import datetime

# --- Flask and Extension Imports ---
from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS # Import for handling Cross-Origin Resource Sharing
from flask_migrate import Migrate # Import for database migrations
# Import ov_client, db, jwt, migrate from extensions.py
from .extensions import db, jwt, ov_client, migrate
# Ensure this line correctly points to your contacts route file:
from .routes.contact_routes import contacts_bp # Should match the actual filename, e.g., contact_routes.py
from .routes.images import images_bp
from .routes.auth import auth_bp # Changed to absolute import
from .routes.audio import audio_bp
from flask_jwt_extended import (
    JWTManager, # JWT Manager class
    create_access_token, # Function to create JWT access tokens
    get_jwt, # Function to get the decoded JWT payload from the request
    get_jwt_identity, # Function to get the identity from the JWT payload
    jwt_required # Decorator to protect routes with JWT authentication
)
# Import configuration classes
from .config import config_by_name, Config

# --- Initialize Extension Objects (Unbound) ---
cors = CORS() # Initialize CORS object

# --- Create Blueprint ---
bp = Blueprint("main", __name__)

# --- Import Models ---
# Import database models
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
    # This is the line that was causing the error because the 'user' table didn't exist
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409
    new_user = User(username=username)
    new_user.set_password(password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error registering user: {str(e)}") # Log the error
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
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    app.config.setdefault('JWT_SECRET_KEY', 'dev-key-for-testing')

    # Explicitly set DB URI from environment variable AFTER loading config object
    # This ensures the env var overrides any defaults from the config object.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
    # Print the URI being used for verification (optional, for debugging)
    print(f"Using database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Import extensions
    from .extensions import db, jwt, cors, migrate, ov_client

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db) # Initialize migrate using the imported object
    jwt.init_app(app)
    # Configure CORS explicitly AFTER creating app and before registering blueprints
    # Allow requests from your frontend development server origin
    cors.init_app(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    # Register JWT token blocklist loader
    @jwt.token_in_blocklist_loader
    def check_if_token_blocklisted(jwt_header, jwt_payload):
        from .models import TokenBlocklist
        jti = jwt_payload["jti"]
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    # --- Database Table Creation ---
    # Create database tables if they don't exist within the application context.
    # This is crucial for in-memory databases which reset on each reload.
    with app.app_context():
        db.create_all()
    # -------------------------------


    app.register_blueprint(bp, url_prefix='/')
    app.register_blueprint(contacts_bp, url_prefix='/api/contacts')
    app.register_blueprint(images_bp, url_prefix='/api/images')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(audio_bp, url_prefix='/api/audio')

    return app

# Entry point for running the Flask application
if __name__ == '__main__':

    print("Forcing Testing Configuration (in-memory database)")

    config_name = 'test'

    app_config = config_by_name.get(config_name)

    app = create_app(app_config)

    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
