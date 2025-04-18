# backend/tests/conftest.py
import pytest
import os
# Use direct imports assuming tests are run from 'backend' or '/app' directory
from backend.main import create_app  # Changed to absolute import
# Import db from extensions directly
from backend.extensions import db as _db  # Added absolute import for db
# Import models directly
from models import Contact, User, TokenBlocklist

@pytest.fixture(scope='session')
def app():
    """Session-wide test Flask application."""
    # Set Testing environment variable BEFORE creating app
    # Ensure this doesn't conflict if create_app also reads FLASK_ENV
    os.environ['FLASK_ENV'] = 'testing'

    # Use a dedicated testing configuration
    # You could have a specific config class or update dict
    config_override = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('TEST_DATABASE_URL', "sqlite:///:memory:"), # In-memory SQLite for tests
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret-key", # Use a fixed secret for tests
        # Disable CSRF protection in tests if you use it
        # "WTF_CSRF_ENABLED": False,
        "SERVER_NAME": "localhost.test" # Helps with url_for generation if needed
    }

    _app = create_app(config_override) # Pass test config if factory supports it

    # Establish an application context before running tests
    ctx = _app.app_context()
    ctx.push()

    yield _app # Provide the app instance to the tests

    # Teardown: pop the context
    ctx.pop()


@pytest.fixture(scope='session')
def db(app):
    """Session-wide database."""
    # Create tables once per session
    _db.create_all()

    yield _db # Provide the database instance to the tests

    # Drop tables once per session
    _db.session.remove() # Ensure session is closed
    _db.drop_all()


@pytest.fixture(scope='function')
def session(db):
    """Creates a new database session for a test."""
    # Connect to the database and create a transaction
    connection = db.engine.connect()
    transaction = connection.begin()

    # Start a session bound to the transaction
    options = dict(bind=connection, binds={})
    sess = db.create_scoped_session(options=options)

    # Replace the default session with this transaction-bound session
    db.session = sess

    yield sess # Provide the session to the test

    # Teardown: rollback the transaction and close the session
    sess.remove()
    transaction.rollback() # Rollback ensures isolation and cleanup after each test
    connection.close()


@pytest.fixture(scope='function')
def client(app):
    """A test client for the app (function scope)."""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """A test runner for the app's Click commands (function scope)."""
    return app.test_cli_runner()

# Sample data fixture using the function-scoped 'session'
@pytest.fixture(scope='function')
def sample_contacts(session): # Inject the function-scoped session
    """Create sample contacts for testing within a transaction."""
    contacts = [
        Contact(first_name="John", last_name="Doe", email="john@example.com"),
        Contact(first_name="Jane", last_name="Smith", email="jane@example.com"),
    ]
    session.add_all(contacts)
    session.commit() # Commit within the transaction managed by 'session' fixture
    # The IDs will be available after commit
    return contacts

# Add similar fixtures for sample users if needed for auth tests
@pytest.fixture(scope='function')
def sample_user(session):
    """Create a sample user for testing."""
    user = User(username="testuser", email="test@example.com")
    user.set_password("password") # Assuming you have a set_password method
    session.add(user)
    session.commit() # Commit within the transaction managed by 'session' fixture
    return user