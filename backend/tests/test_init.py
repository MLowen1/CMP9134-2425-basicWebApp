import pytest
from unittest.mock import patch, MagicMock
import os
import importlib
# Import the specific create_app function being tested
from backend import create_app as backend_create_app
# Import config classes to pass directly if needed, or use names
from backend.config import DevelopmentConfig, TestingConfig, ProductionConfig, config_by_name

def test_create_app_development():
    # Pass the configuration name directly
    app = backend_create_app('dev')
    assert app.config['DEBUG'] is True
    # assert isinstance(app.config, DevelopmentConfig) # Removed incorrect check

def test_create_app_testing():
    # Pass the configuration name directly
    app = backend_create_app('test')
    assert app.config['TESTING'] is True
    # assert isinstance(app.config, TestingConfig) # Removed incorrect check

def test_create_app_production():
    # Temporarily set the environment variable needed by ProductionConfig
    original_db_url = os.environ.get('DATABASE_URL')
    os.environ['DATABASE_URL'] = 'sqlite:///prod_test.db' # Use a dummy value for the test
    
    try:
        # Pass the configuration name directly
        app = backend_create_app('prod')
        assert app.config['DEBUG'] is False
        assert app.config['TESTING'] is False
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///prod_test.db'
        # assert isinstance(app.config, ProductionConfig) # Removed incorrect check
    finally:
        # Clean up the environment variable
        if original_db_url is None:
            # Check if the key exists before deleting to avoid KeyError
            if 'DATABASE_URL' in os.environ:
                del os.environ['DATABASE_URL']
        else:
            os.environ['DATABASE_URL'] = original_db_url

def test_create_app_invalid_config_name():
    """Test create_app with an invalid configuration name."""
    with pytest.raises(ValueError, match="Invalid configuration name: invalid_name"):
        backend_create_app('invalid_name')

def test_create_app_invalid_config_type():
    """Test create_app with an invalid configuration type."""
    with pytest.raises(TypeError, match="must be a string name or a Config class/object"):
        backend_create_app(123) # Pass an integer, which is invalid

# Test for RuntimeError when DATABASE_URL is missing in production
# This requires careful environment manipulation
def test_create_app_prod_missing_db_url():
    """Test create_app('prod') raises RuntimeError if DATABASE_URL is not set."""
    original_db_url = os.environ.pop('DATABASE_URL', None)
    original_flask_env = os.environ.pop('FLASK_ENV', None)
    os.environ['FLASK_ENV'] = 'prod' # Simulate production environment

    try:
        # Expect RuntimeError because DATABASE_URL is missing
        with pytest.raises(RuntimeError, match="DATABASE_URL environment variable must be set"):
            # Use 'prod' name which triggers the check in create_app
            app = backend_create_app('prod')
    finally:
        # Restore environment variables
        if original_db_url is not None:
            os.environ['DATABASE_URL'] = original_db_url
        if original_flask_env is not None:
            os.environ['FLASK_ENV'] = original_flask_env
        elif 'FLASK_ENV' in os.environ:
             del os.environ['FLASK_ENV'] # Clean up if it wasn't set before

# Optional: Test passing a config object directly
def test_create_app_with_object():
    app = backend_create_app(TestingConfig)
    assert app.config['TESTING'] is True
    # assert isinstance(app.config, TestingConfig) # Removed incorrect check
