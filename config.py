import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Determine the base directory of the application
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add other default configurations here
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-jwt') # Example JWT secret key
    JWT_ACCESS_TOKEN_EXPIRES = 3600 # Example: 1 hour
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'dev.db')
    # Example: Override JWT expiration for development
    JWT_ACCESS_TOKEN_EXPIRES = 1800 # 30 minutes in dev


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    # Make sure SQLite uses an in-memory database for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    # Use shorter token expiration for testing if needed
    JWT_ACCESS_TOKEN_EXPIRES = 60 # 1 minute for testing


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Ensure DATABASE_URL is set in the production environment
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'prod.db') # Fallback, but should be properly configured


# Dictionary to access configuration classes by name
config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    testing=TestingConfig,  # Add alias for 'testing'
    prod=ProductionConfig,
    default=DevelopmentConfig # Default to development if FLASK_ENV is not set
)

# Function to get the secret key, useful for JWT
def key():
    return Config.SECRET_KEY