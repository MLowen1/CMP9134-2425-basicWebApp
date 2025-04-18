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

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secret_key')
    DEBUG = False
    TESTING = False
    # Add other configuration variables like database URI, etc.
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///default.db') # Base class doesn't define it
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add JWT settings to base config for consistency
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "default-insecure-secret-key-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dev.db'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    # Use a separate database for testing if needed
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Ensure SECRET_KEY is set securely in production environment
    SECRET_KEY = os.environ.get('SECRET_KEY') # Don't use default in production
    # Add SQLALCHEMY_DATABASE_URI for production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # Should be set in environment

# Optional: Dictionary to access configs by name
config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)