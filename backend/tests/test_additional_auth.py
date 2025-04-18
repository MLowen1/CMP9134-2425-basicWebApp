import json
import pytest
from unittest.mock import patch, MagicMock
from itsdangerous import SignatureExpired # <-- Import SignatureExpired
# Import db from extensions to use db.session.get
from backend.models import User, db
# Import the helper function to get the serializer
from backend.routes.auth import get_reset_serializer

# Skip this test as email sending is not implemented yet
@pytest.mark.skip(reason="Email sending for password reset not implemented")
def test_request_password_reset(app, client, authenticated_user):
    data = {'email': 'test@example.com'}
    
    with patch('backend.routes.auth.mail.send') as mock_send:
        response = client.post('/api/auth/request-password-reset', 
                               data=json.dumps(data),
                               content_type='application/json')
        
        assert response.status_code == 200
        assert json.loads(response.data)['message'] == 'Password reset email sent'
        mock_send.assert_called_once()

# Skip this test as email sending is not implemented yet
@pytest.mark.skip(reason="Email sending for password reset not implemented")
def test_request_password_reset_invalid_email(app, client):
    data = {'email': 'nonexistent@example.com'}
    
    with patch('backend.routes.auth.mail.send') as mock_send:
        response = client.post('/api/auth/request-password-reset', 
                               data=json.dumps(data),
                               content_type='application/json')
        
        assert response.status_code == 404
        assert json.loads(response.data)['error'] == 'Email not found'
        mock_send.assert_not_called()

def test_reset_password(app, client, authenticated_user):
    with app.app_context():
        # Use the helper function to get the serializer instance
        serializer = get_reset_serializer()
        token = serializer.dumps({'user_id': authenticated_user.id})
        
        data = {
            'token': token,
            'new_password': 'newSecurePassword123'
        }
        
        response = client.post('/api/auth/reset-password', 
                              data=json.dumps(data),
                              content_type='application/json')
        
        assert response.status_code == 200
        assert json.loads(response.data)['message'] == 'Password updated successfully'
        
        # Verify password was actually changed using db.session.get
        user = db.session.get(User, authenticated_user.id) # Changed from User.query.get
        assert user.check_password('newSecurePassword123')

def test_reset_password_invalid_token(app, client):
    data = {
        'token': 'invalid-token',
        'new_password': 'newSecurePassword123'
    }
    
    response = client.post('/api/auth/reset-password', 
                          data=json.dumps(data),
                          content_type='application/json')
    
    assert response.status_code == 400
    assert 'error' in json.loads(response.data)

def test_auth_status_unauthenticated(client):
    """Test the /api/auth/status route when not logged in."""
    response = client.get('/api/auth/status')
    assert response.status_code == 200
    assert response.get_json() == {'logged_in_as': None}

def test_auth_status_authenticated(client, authenticated_user):
    """Test the /api/auth/status route when logged in."""
    response = client.get('/api/auth/status',
                          headers={'Authorization': f'Bearer {authenticated_user.token}'})
    assert response.status_code == 200
    # Assuming authenticated_user fixture provides user with username 'testuser'
    assert response.get_json() == {'logged_in_as': 'testuser'}

def test_reset_password_expired_token(app, client, authenticated_user):
    """Test password reset with an expired token."""
    with app.app_context():
        serializer = get_reset_serializer()
        # Create a token that expires immediately (or very quickly)
        token = serializer.dumps({'user_id': authenticated_user.id}, salt='reset-salt') # Use salt if configured

    # Simulate time passing beyond expiration (e.g., mock time or use a short max_age)
    # For simplicity, we rely on the default max_age being reasonably short or test the logic
    # If max_age is 1 hour, this test might need time mocking or adjusting max_age in config

    # A more direct way without time mocking is to test the exception handling
    with patch('backend.routes.auth.get_reset_serializer') as mock_get_serializer:
        mock_serializer_instance = MagicMock()
        # Make loads raise SignatureExpired
        mock_serializer_instance.loads.side_effect = SignatureExpired("Token expired")
        mock_get_serializer.return_value = mock_serializer_instance

        data = {
            'token': 'dummy-token-value', # Value doesn't matter as loads is mocked
            'new_password': 'newPassword123'
        }
        response = client.post('/api/auth/reset-password',
                              data=json.dumps(data),
                              content_type='application/json')

        assert response.status_code == 400
        assert 'expired' in response.get_json().get('error', '').lower()
