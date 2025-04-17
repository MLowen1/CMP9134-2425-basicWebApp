import pytest
from backend import create_app, db
from models import Contact

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def sample_contacts(app):
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