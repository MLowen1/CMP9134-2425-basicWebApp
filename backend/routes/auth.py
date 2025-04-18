from flask import Blueprint, request, jsonify, current_app
from backend.extensions import db, jwt # Assuming db and jwt might be needed
from backend.models import User, TokenBlocklist # Assuming models are needed
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
import datetime
# Add imports for password reset
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

auth_bp = Blueprint('auth', __name__)

# --- Password Reset Serializer ---
# Ensure the secret key is fetched correctly from the app config
# We define a function to create the serializer within the app context later if needed,
# or initialize it carefully. For simplicity here, we'll use current_app later.
# reset_password_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY']) # Needs app context

# Helper function to get the serializer
def get_reset_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

# Example placeholder route if needed, otherwise this file can just define the blueprint
@auth_bp.route('/status', methods=['GET'])
@jwt_required(optional=True) # Example: Check status, optionally requiring JWT
def status():
    """Placeholder route to check auth status."""
    current_user_id = get_jwt_identity()
    if current_user_id:
        user = db.session.get(User, current_user_id)
        return jsonify(logged_in_as=user.username), 200
    else:
        return jsonify(logged_in_as=None), 200

# Add the @me endpoint that returns the current user's information
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get the currently authenticated user's information."""
    # Get the user ID from the JWT
    current_user_id = get_jwt_identity()
    
    # Look up the user in the database
    user = db.session.get(User, current_user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Return the user information
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200

# --- Add Password Reset Route ---
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset user password using a token."""
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    serializer = get_reset_serializer()
    try:
        # Deserialize the token, max_age in seconds (e.g., 1 hour)
        payload = serializer.loads(token, max_age=3600)
        user_id = payload.get('user_id')
        if not user_id:
             raise BadSignature("Invalid payload in token") # Treat missing user_id as bad signature

        user = db.session.get(User, user_id)
        if not user:
            # Although unlikely if token is valid, handle case where user might have been deleted
            return jsonify({"error": "User not found"}), 404 

        # Update the password
        user.set_password(new_password)
        db.session.commit()
        return jsonify({"message": "Password updated successfully"}), 200

    except SignatureExpired:
        return jsonify({"error": "Password reset token has expired"}), 400
    except BadSignature:
        # This catches invalid tokens, tampered tokens, or missing user_id
        return jsonify({"error": "Invalid or malformed password reset token"}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error resetting password: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

# Consider moving register, login, logout logic from main.py to here
# Example:
# @auth_bp.route("/register", methods=["POST"])
# def register():
#     # ... registration logic ...
#     pass

# @auth_bp.route("/login", methods=["POST"])
# def login():
#     # ... login logic ...
#     pass

# @auth_bp.route("/logout", methods=["POST"])
# @jwt_required()
# def logout():
#     # ... logout logic ...
#     pass
