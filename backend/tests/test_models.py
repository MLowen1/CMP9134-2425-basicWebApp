import pytest
from models import Contact, User

# Verifies that the Contact model correctly stores data and tests that the to_JSON() method returns the expected format
def test_contact_model():
    """Test Contact model creation and conversion to JSON."""
    contact = Contact(first_name="Test", last_name="User", email="test@test.com")

    # Test that the properties are set correctly
    assert contact.first_name == "Test"
    assert contact.last_name == "User"
    assert contact.email == "test@test.com"

    # Test the to_json method
    contact_json = contact.to_json()
    assert contact_json["firstName"] == "Test"
    assert contact_json["lastName"] == "User"
    assert contact_json["email"] == "test@test.com"
    
def test_user_password_hashing_and_serialization():
    """Test setting and checking password hash, and JSON serialization for User."""
    user = User(username="testuser")
    # Initially, no password hash is set
    assert getattr(user, '_password_hash', None) in (None, '')
    # Set password and verify hashing
    user.set_password("mysecret")
    assert user.check_password("mysecret") is True
    assert user.check_password("wrongpassword") is False
    # to_json should include id and username, but not password hash
    user_json = user.to_json()
    assert "username" in user_json and user_json["username"] == "testuser"
    assert "id" in user_json
    # Ensure password hash is not exposed
    assert "_password_hash" not in user_json and "password_hash" not in user_json