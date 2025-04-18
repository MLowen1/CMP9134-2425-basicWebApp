# File: backend/tests/test_auth_endpoints.py

import json
import pytest
# Assuming models are now imported directly from the 'models' file
# and User/TokenBlocklist are defined there
from models import User, TokenBlocklist  
from flask import url_for

# --- Registration Tests ---

def test_register_success(client):
    """Test successful user registration."""
    payload = {"username": "alice", "password": "password123"}
    response = client.post(
        '/register',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.get_json()}"
    data = response.get_json()
    # Correct expected message
    assert data.get("message") == "User registered successfully!", "Incorrect success message" 
    assert "access_token" in data, "Access token missing in response"

    # Optional: Verify user exists in DB (requires db fixture)
    # user = User.query.filter_by(username="alice").first()
    # assert user is not None

def test_register_missing_fields(client):
    """Test registration with missing fields."""
    # Missing password
    response = client.post('/register', data=json.dumps({"username": "bob"}), content_type='application/json')
    assert response.status_code == 400, "Should fail with 400 if password missing"
    assert "Username and password are required" in response.get_json().get("message", "")

    # Missing username
    response = client.post('/register', data=json.dumps({"password": "pw"}), content_type='application/json')
    assert response.status_code == 400, "Should fail with 400 if username missing"
    assert "Username and password are required" in response.get_json().get("message", "")

def test_register_duplicate_username(client):
    """Test registration with an existing username."""
    # Register first time
    payload = {"username": "charlie", "password": "pw"}
    client.post('/register', data=json.dumps(payload), content_type='application/json')
    
    # Register again with same username
    response = client.post(
        '/register',
        data=json.dumps({"username": "charlie", "password": "newpw"}),
        content_type='application/json'
    )
    # Correct expected status code
    assert response.status_code == 409, f"Expected 409 Conflict, got {response.status_code}" 
    assert "Username already exists" in response.get_json().get("message", "")

# --- Login Tests ---

def test_login_success(client):
    """Test successful login."""
    # Register user first
    reg_payload = {"username": "dave", "password": "pw"}
    client.post('/register', data=json.dumps(reg_payload), content_type='application/json')
    
    # Login with correct credentials
    login_payload = {"username": "dave", "password": "pw"}
    response = client.post(
        '/login',
        data=json.dumps(login_payload),
        content_type='application/json'
    )
    # Correct expected status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.get_json()}" 
    data = response.get_json()
    assert data.get("message") == "Login succeeded", "Incorrect login message"
    assert "access_token" in data, "Access token missing in login response"

@pytest.mark.parametrize("creds", [
    ({"username": "eve", "password": "wrong"}),       # Correct user, wrong password
    ({"username": "nonexistent", "password": "pw"}), # Non-existent user
])
def test_login_failures(client, creds):
    """Test login with invalid credentials or non-existent user."""
    # Setup user for the first case ('eve')
    if creds["username"] == "eve":
        client.post(
            '/register',
            data=json.dumps({"username": "eve", "password": "correct"}),
            content_type='application/json'
        )
        
    response = client.post(
        '/login',
        data=json.dumps(creds),
        content_type='application/json'
    )
    # Correct expected status code
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}" 
    assert "Bad username or password" in response.get_json().get("message", "")

import pytest
import json
from flask import url_for

def test_login_missing_fields(client):
    """Test login with missing fields."""
    # Missing password
    response = client.post('/login', json={"username": "frank"})
    assert response.status_code == 401
    
    # Missing username
    response = client.post('/login', json={"password": "secret"})
    assert response.status_code == 401
    
    # Missing both
    response = client.post('/login', json={})
    assert response.status_code == 401

def test_me_and_logout_flow(client, app):
    """Test accessing user info, logging out, and token blocklisting."""
    # Make sure we have an active app context
    with app.app_context():
        # Register and obtain token
        payload = {"username": "tester", "password": "secret"}
        reg_resp = client.post('/register', json=payload)
        
        assert reg_resp.status_code == 201
        access_token = reg_resp.json.get('access_token')
        
        # Test @me endpoint with token
        me_resp = client.get('/@me', 
                             headers={'Authorization': f'Bearer {access_token}'})
        
        assert me_resp.status_code == 200
        assert me_resp.json.get('username') == 'tester'
        
        # Test logout
        logout_resp = client.post('/logout', 
                                  headers={'Authorization': f'Bearer {access_token}'})
        
        assert logout_resp.status_code == 200
        
        # Try using the token after logout (should be blocked)
        blocked_resp = client.get('/@me', 
                                  headers={'Authorization': f'Bearer {access_token}'})
        
        assert blocked_resp.status_code == 401

def test_me_requires_token(client):
    """Test accessing /@me without providing a token."""
    resp = client.get('/@me')
    assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}"

def test_me_requires_token(client):
    """Test accessing /api/auth/me without providing a token."""
    # Use the correct endpoint URL based on blueprint registration
    resp = client.get('/api/auth/me')
    # Correct expected status code
    assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}"
    # Check for message indicating missing token
    assert "Missing Authorization Header" in resp.get_json().get("msg", "")


def test_logout_requires_token(client):
    """Test accessing /logout without providing a token."""
    resp = client.post('/logout')
     # Correct expected status code
    assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}"
    assert "Missing Authorization Header" in resp.get_json().get("msg", "")