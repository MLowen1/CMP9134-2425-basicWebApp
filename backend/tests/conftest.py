import pytest
from config import app, db
from models import Contact
import main

#Creates a test client for the Flask app and sets up an in-memory database for testing.
@pytest.fixture
def client():
    """Create a test client for the app with an in-memory database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

#Created test data
@pytest.fixture
def sample_contacts():
    """Create sample contacts for testing."""
    contacts = [
        Contact(first_name="John", last_name="Doe", email="john@example.com"),
        Contact(first_name="Jane", last_name="Smith", email="jane@example.com"),
        Contact(first_name="Bob", last_name="Johnson", email="bob@example.com")
    ]

    with app.app_context():
        for contact in contacts:
            db.session.add(contact)
        db.session.commit()
    return contacts