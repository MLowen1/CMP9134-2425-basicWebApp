import json
import pytest

from models import User

def test_register_success(client):
    # Register a new user
    payload = {"username": "alice", "password": "password123"}
    response = client.post(
        '/register',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered!"
    assert "access_token" in data and isinstance(data["access_token"], str)
    # Verify user in database
    with client.application.app_context():
        u = User.query.filter_by(username="alice").first()
        assert u is not None

def test_register_missing_fields(client):
    # Missing password
    response = client.post(
        '/register',
        data=json.dumps({"username": "bob"}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "required" in data.get("message", "")

def test_register_duplicate_username(client):
    # Register first time
    client.post(
        '/register',
        data=json.dumps({"username": "charlie", "password": "pw"}),
        content_type='application/json'
    )
    # Register again with same username
    response = client.post(
        '/register',
        data=json.dumps({"username": "charlie", "password": "newpw"}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data.get("message") == "Username already exists"

def test_login_success(client):
    # Register user
    client.post(
        '/register',
        data=json.dumps({"username": "dave", "password": "pw"}),
        content_type='application/json'
    )
    # Login with correct credentials
    response = client.post(
        '/login',
        data=json.dumps({"username": "dave", "password": "pw"}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("message") == "Login succeeded"
    assert "access_token" in data and isinstance(data["access_token"], str)

@pytest.mark.parametrize("creds", [
    ({"username": "eve", "password": "wrong"}),
    ({"username": "nonexistent", "password": "pw"}),
])
def test_login_failures(client, creds):
    # Setup user for first case
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
    assert response.status_code == 401
    data = response.get_json()
    assert data.get("message") == "Bad username or password"

def test_login_missing_fields(client):
    # Missing password
    response = client.post(
        '/login',
        data=json.dumps({"username": "frank"}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "required" in data.get("message", "")
    
def test_me_and_logout_flow(client):
    # Register and obtain token
    payload = {"username": "tester", "password": "secret"}
    reg_resp = client.post('/register', data=json.dumps(payload), content_type='application/json')
    assert reg_resp.status_code == 201, f"Registration failed: {reg_resp.get_json()}"
    token = reg_resp.get_json().get("access_token")
    assert token, f"Token missing in response: {reg_resp.get_json()}"
    auth_header = {"Authorization": f"Bearer {token}"}

    # Access @me endpoint
    me_resp = client.get('/@me', headers=auth_header)
    assert me_resp.status_code == 200, f"Accessing /@me failed: {me_resp.get_json()}"
    user_data = me_resp.get_json()
    assert user_data.get("username") == "tester", "Username mismatch"
    assert "id" in user_data

    # Logout
    logout_resp = client.post('/logout', headers=auth_header)
    assert logout_resp.status_code == 200, f"Logout failed: {logout_resp.get_json()}"
    assert logout_resp.get_json().get("message") == "Logout successful"

    # Token should now be invalid
    me_resp2 = client.get('/@me', headers=auth_header)
    assert me_resp2.status_code == 401, f"Token should be invalid: {me_resp2.get_json()}"
    err = me_resp2.get_json()
    assert err is not None
    
def test_me_requires_token(client):
    # Access /@me without token should be rejected
    resp = client.get('/@me')
    assert resp.status_code == 401

def test_logout_requires_token(client):
    # Logout without token should be rejected
    resp = client.post('/logout')
    assert resp.status_code == 401