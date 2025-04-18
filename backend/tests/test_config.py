import os
import pytest
# Import create_app to test config loading
from backend import create_app 
from backend.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig

def test_base_config():
    config = Config()
    assert not config.DEBUG
    assert not config.TESTING
    assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    assert config.JWT_SECRET_KEY == os.environ.get('JWT_SECRET_KEY', 'default-insecure-secret-key-change-me')
    # Update the expected default SECRET_KEY value
    assert config.SECRET_KEY == os.environ.get('SECRET_KEY', 'a_default_secret_key')

def test_dev_config():
    config = DevelopmentConfig()
    assert config.DEBUG
    assert config.SQLALCHEMY_DATABASE_URI.startswith('sqlite:///')
    
def test_testing_config():
    config = TestingConfig()
    assert config.TESTING
    assert config.SQLALCHEMY_DATABASE_URI == 'sqlite:///:memory:'
    
def test_production_config():
    # Temporarily set environment variables for testing
    original_db_url = os.environ.get('DATABASE_URL')
    test_db_url = 'postgresql://test:test@localhost/test'
    os.environ['DATABASE_URL'] = test_db_url
    
    try:
        # Create an app instance using the 'prod' config name
        # This uses the logic in create_app to set the URI
        app = create_app('prod') 
        
        # Check the config values on the app instance
        assert not app.config['DEBUG']
        assert not app.config['TESTING']
        assert app.config['SQLALCHEMY_DATABASE_URI'] == test_db_url
    finally:
        # Clean up environment
        if original_db_url is None:
            if 'DATABASE_URL' in os.environ:
                 del os.environ['DATABASE_URL']
        else:
             os.environ['DATABASE_URL'] = original_db_url
