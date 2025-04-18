import json
import pytest
from unittest.mock import patch, MagicMock
import os
from backend.models import User, db

# Test for lines 50-66: create_admin_user function - REMOVED as function not in main.py
# def test_create_admin_user(app):
#     ...

# Test for lines 71-77: handle_error function - REMOVED as function not in main.py
# def test_handle_error(app):
#     ...

# Test for lines 84-95: init_db function - REMOVED as function not in main.py
# def test_init_db(app):
#     ...

# Test for lines 102-107: index route
def test_index_route(app):
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        # Check for the specific message returned by the index route in main.py's blueprint
        assert b'API is running' in response.data 

# Test for lines 112-161: Various API routes
def test_api_routes(app):
    with app.test_client() as client:
        # Test GET /api route
        response = client.get('/api')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'API is running'
        
        # Test GET /api/protected route (unauthorized)
        response = client.get('/api/protected')
        assert response.status_code == 401
        
        # Test GET /api/protected route (authorized)
        # Create a test user within an app context
        with app.app_context():
            user = User(
                username='testuser', 
                email='testuser@example.com' # Email is optional in model, but good to include
            )
            user.set_password('password123') # Set password using the method
            db.session.add(user)
            db.session.commit()
            
        # Now, outside the app_context, perform the login request
        response = client.post(
            '/login', # Use the correct login route from bp
            data=json.dumps({
                'username': 'testuser', # Use username for login
                'password': 'password123'
            }),
            content_type='application/json'
        )
        # Check if login was successful before getting token
        assert response.status_code == 200, f"Login failed: {response.get_json()}"
        token = json.loads(response.data)['access_token']
        
        # Test protected route with token
        response = client.get(
            '/api/protected', # Use the correct protected route from bp
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'This is a protected route'
        # Verify the username returned matches the logged-in user
        assert data['logged_in_as'] == 'testuser' 

# Test for lines 174, 177: configure_routes function - REMOVED as function not in main.py
# def test_configure_routes(app):
#     ...
