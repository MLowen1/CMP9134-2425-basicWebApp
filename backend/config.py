# File: backend/config.py

import os
from datetime import timedelta

# --- Configuration Settings ---
# These settings will be loaded by app.config.from_pyfile('config.py') 
# or environment variables within the create_app factory.

# Database Configuration
# Use DATABASE_URL from environment if available, otherwise default to SQLite
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///appdatabase.db") 
SQLALCHEMY_DATABASE_URI = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False 

# JWT Configuration
# Load secret key from environment variable OR use a default (INSECURE FOR PRODUCTION)
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "default-insecure-secret-key-change-me") 
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1) # Example: Token expires in 1 hour

# --- No global token_blocklist or Flask app/extension initialization here ---