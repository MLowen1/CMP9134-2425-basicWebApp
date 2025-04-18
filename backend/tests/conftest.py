import os
import sys
import pytest
import tempfile
import signal
import atexit
import gc

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the app factory and extensions
from backend.main import create_app
from backend.extensions import db
from backend.models import User, Contact
# Import create_access_token
from flask_jwt_extended import create_access_token

# Session-level teardown function to clean up resources
@pytest.fixture(scope="session", autouse=True)
def cleanup_after_tests(request):
    """Cleanup function that runs after all tests complete."""
    
    def finalize():
        # Force garbage collection to clean up any lingering objects
        gc.collect()
        
        # Close any open database connections
        try:
            db.session.remove()
            db.engine.dispose()
        except:
            pass
            
        # Print confirmation for debugging
        print("Teardown complete - cleaned up all resources")
    
    # Register the finalize function to run when the session ends
    request.addfinalizer(finalize)
    
    # Also register with atexit to ensure it runs even on abnormal termination
    atexit.register(finalize)
    
    # Set up signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        print(f"Received signal {signum}, cleaning up...")
        finalize()
        # Re-raise the signal to allow the default handler to run
        signal.signal(signum, signal.SIG_DFL)
        signal.raise_signal(signum)
    
    # Register signal handlers for common termination signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    return

@pytest.fixture
def app():
    """Create a Flask application for testing.""" 
    # Create a test configuration
    test_config = {
        "TESTING": True,
        "DEBUG": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret-key"
    }
    
    # Create the app
    app = create_app(test_config)
    
    # Create all tables
    with app.app_context():
        db.create_all()
        print("Created test database tables")
    
    # Return the app to the test
    yield app
    
    # Clean up
    with app.app_context():
        db.session.remove()
        db.drop_all()
        print("Dropped test database tables")

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def sample_contacts(app):
    """Create sample contacts for testing."""
    contacts = []
    with app.app_context():
        # Create two sample contacts
        contacts = [
            Contact(first_name="John", last_name="Doe", email="john@example.com"),
            Contact(first_name="Jane", last_name="Smith", email="jane@example.com")
        ]
        db.session.add_all(contacts)
        db.session.commit()
        
        # Save their IDs
        contact_ids = [c.id for c in contacts]
    
    yield contacts
    
    # Clean up
    with app.app_context():
        for contact_id in contact_ids:
            contact = db.session.get(Contact, contact_id)
            if contact:
                db.session.delete(contact)
        db.session.commit()

@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    with app.app_context():
        user = User(username="testuser")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    # Reload user within context to ensure it's bound to the session
    with app.app_context():
        user = db.session.get(User, user_id)
        yield user # Yield the user object bound to the session
    
    # Clean up
    with app.app_context():
        user_to_delete = db.session.get(User, user_id)
        if user_to_delete:
            db.session.delete(user_to_delete)
        db.session.commit()

@pytest.fixture
def authenticated_user(app, sample_user):
    """Create a sample user and generate an access token."""
    with app.app_context():
        # Generate token using the user's ID
        access_token = create_access_token(identity=str(sample_user.id))
        # Attach the token to the user object for easy access in tests
        sample_user.token = access_token 
    yield sample_user
    # Cleanup is handled by the sample_user fixture