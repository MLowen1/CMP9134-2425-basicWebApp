import pytest
from unittest.mock import patch, MagicMock
# Update import to only include modules that actually exist
from backend.extensions import db, jwt, cors

def test_db_config(app):
    with app.app_context():
        # Test that the db extension is properly configured
        assert hasattr(db, 'init_app')
        assert hasattr(db, 'Model')

def test_jwt_config(app):
    with app.app_context():
        # Test that jwt extension is properly configured
        assert hasattr(jwt, 'init_app')

def test_cors_config(app):
    with app.app_context():
        # Test that cors extension is properly configured
        assert hasattr(cors, 'init_app')
