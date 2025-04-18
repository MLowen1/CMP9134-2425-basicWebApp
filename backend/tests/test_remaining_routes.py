import json
import pytest
from unittest.mock import patch, MagicMock
from backend.models import Contact

# Tests for contact_routes.py missing branches
def test_get_contact_not_found(app, client, authenticated_user):
    # Test getting a non-existent contact
    response = client.get('/api/contacts/999', 
                         headers={'Authorization': f'Bearer {authenticated_user.token}'})
    
    assert response.status_code == 404
    # Assuming the contact routes are now under /api/contacts
    # Check the actual error message format from your route
    assert 'not found' in json.loads(response.data).get('message', '').lower()

def test_create_contact_validation_error(app, client, authenticated_user):
    # Test with missing required fields (adjust based on your actual model/validation)
    # Assuming firstName, lastName, email are required
    data = {
        'firstName': '',  # Empty first name should fail validation
        'lastName': 'Test',
        'email': 'test@example.com',
        # 'phone': '1234567890' # Optional
    }
    
    response = client.post('/api/contacts',
                          headers={'Authorization': f'Bearer {authenticated_user.token}'},
                          data=json.dumps(data),
                          content_type='application/json')
    
    assert response.status_code == 400
    # Check the actual error message format from your route
    response_data = json.loads(response.data)
    assert 'cannot be empty' in response_data.get('message', '').lower() # Check for the specific validation message

def test_update_contact_validation_error(app, client, authenticated_user, sample_contacts):
    # Use one of the sample contacts created by the fixture
    contact_to_update = sample_contacts[0]
    contact_id = contact_to_update.id
    
    # Now try to update with invalid data (e.g., empty required field)
    update_data = {
        'firstName': '',  # Empty first name should fail validation
        'email': 'valid@example.com', # Keep email valid or test separately
    }
    
    response = client.put(f'/api/contacts/{contact_id}',
                         headers={'Authorization': f'Bearer {authenticated_user.token}'},
                         data=json.dumps(update_data),
                         content_type='application/json')
    
    assert response.status_code == 400 # Expect 400 for validation error
    # Check the actual error message format from your route
    response_data = json.loads(response.data)
    assert 'cannot be empty' in response_data.get('message', '').lower() # Check for the specific validation message

def test_delete_nonexistent_contact(app, client, authenticated_user):
    response = client.delete(f'/api/contacts/999',
                           headers={'Authorization': f'Bearer {authenticated_user.token}'})
    
    assert response.status_code == 404
    # Check the actual error message format from your route
    assert 'not found' in json.loads(response.data).get('message', '').lower()

# Tests for images.py
def test_search_images(client, authenticated_user):
    # Mock the OpenverseClient where it's used in the route module
    with patch('backend.routes.images.ov_client') as mock_ov_client: # Changed patch target
        # Configure the mock's search_images method
        mock_ov_client.search_images.return_value = {
            'results': [
                {'id': 'test1', 'title': 'Test Image 1', 'url': 'url1', 'thumbnail': 'thumb1'},
                {'id': 'test2', 'title': 'Test Image 2', 'url': 'url2', 'thumbnail': 'thumb2'}
            ],
            'result_count': 2
        }
        
        response = client.get('/api/images/search?q=test',
                            headers={'Authorization': f'Bearer {authenticated_user.token}'})
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        # Check the structure returned by your actual endpoint
        assert 'results' in response_data
        assert len(response_data['results']) == 2
        assert response_data['results'][0]['title'] == 'Test Image 1'
        # Verify the mock was called
        mock_ov_client.search_images.assert_called_once_with('test')

def test_search_images_missing_query(client, authenticated_user):
    """Test image search without providing the 'q' parameter."""
    response = client.get('/api/images/search', # Missing ?q=...
                        headers={'Authorization': f'Bearer {authenticated_user.token}'})
    assert response.status_code == 400
    assert 'parameter \'q\' is required' in response.get_json().get('error', '').lower()

def test_search_images_client_exception(client, authenticated_user):
    """Test image search when the Openverse client raises an unexpected exception."""
    with patch('backend.routes.images.ov_client') as mock_ov_client:
        # Configure the mock to raise a generic Exception
        mock_ov_client.search_images.side_effect = Exception("Unexpected client error")

        response = client.get('/api/images/search?q=test',
                            headers={'Authorization': f'Bearer {authenticated_user.token}'})

        assert response.status_code == 500
        assert 'unexpected error occurred' in response.get_json().get('error', '').lower()
        mock_ov_client.search_images.assert_called_once_with('test')
