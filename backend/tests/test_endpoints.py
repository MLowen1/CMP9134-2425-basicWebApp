import json
import pytest
from backend.models import Contact
from backend.extensions import db

def test_get_contacts(client, sample_contacts, app):
    """Test getting the list of contacts."""
    with app.app_context():
        response = client.get('/api/contacts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2

def test_create_contact(client, app):
    """Test creating a new contact."""
    with app.app_context():
        new_contact = {
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com"
        }
        
        response = client.post('/api/contacts', json=new_contact)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data.get('firstName') == 'Test'
        assert data.get('lastName') == 'User'
        assert data.get('email') == 'test@example.com'

def test_update_contact(client, app, sample_contacts):
    """Test updating an existing contact."""
    with app.app_context():
        # Get a contact ID from the database
        contact_id = sample_contacts[0].id
        
        updated_data = {
            "firstName": "UpdatedFirstName",
            "lastName": "UpdatedLastName",
            "email": "updated@example.com"
        }
        
        response = client.put(f'/api/contacts/{contact_id}', json=updated_data)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data.get('firstName') == 'UpdatedFirstName'
        
        # Use db.session.get to verify the update
        updated_contact = db.session.get(Contact, contact_id)
        assert updated_contact.first_name == 'UpdatedFirstName'

def test_delete_contact(client, app, sample_contacts):
    """Test deleting a contact."""
    with app.app_context():
        # Get a contact ID from the database
        contact_id = sample_contacts[0].id
        
        response = client.delete(f'/api/contacts/{contact_id}')
        
        assert response.status_code == 200
        # Verify the contact was deleted
        assert db.session.get(Contact, contact_id) is None