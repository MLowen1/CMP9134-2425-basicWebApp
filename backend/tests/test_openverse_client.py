import pytest
from unittest.mock import patch, MagicMock
# Import the specific exception
import requests 
from backend.openverse_client import OpenverseClient

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {
        'result_count': 1,
        'results': [
            {
                'id': 'test-id',
                'title': 'Test Image',
                'creator': 'Test Creator',
                'url': 'https://example.com/image.jpg',
                'thumbnail': 'https://example.com/thumbnail.jpg',
                'license': 'CC BY',
                'license_version': '4.0'
            }
        ]
    }
    return mock

def test_search_images(mock_response):
    with patch('requests.get', return_value=mock_response):
        client = OpenverseClient()
        results_data = client.search_images('test query') # Rename variable for clarity
        
        # Assert based on the structure returned by the mock
        assert 'results' in results_data 
        assert isinstance(results_data['results'], list)
        assert len(results_data['results']) == 1 
        assert results_data['results'][0]['title'] == 'Test Image'
        assert results_data['results'][0]['creator'] == 'Test Creator'

def test_search_images_with_params(mock_response):
    with patch('requests.get', return_value=mock_response):
        client = OpenverseClient()
        results_data = client.search_images('test query', page=2, page_size=10, license_type='commercial') # Rename variable
        
        # Assert based on the structure returned by the mock
        assert 'results' in results_data
        assert isinstance(results_data['results'], list)
        assert len(results_data['results']) == 1 # Check length of the inner list

def test_search_images_error():
    error_response = MagicMock()
    error_response.status_code = 500
    # Configure raise_for_status to raise an HTTPError for search error
    error_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error") 
    
    with patch('requests.get', return_value=error_response):
        client = OpenverseClient()
        results = client.search_images('test query')
        
        # Assert that the result is a dictionary containing the 'error' key
        assert isinstance(results, dict)
        assert 'error' in results 
        assert "Error searching images" in results['error']

def test_get_auth_token(mock_response): # Renamed test function for clarity
    with patch('requests.post') as mock_post:
        mock_token_response = MagicMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {'access_token': 'test-token', 'expires_in': 3600}
        mock_post.return_value = mock_token_response
        
        client = OpenverseClient()
        token = client._get_auth_token() # Changed method call
        
        assert token == 'test-token' # Assert the token value

def test_get_auth_token_error(): # Renamed test function for clarity
    with patch('requests.post') as mock_post:
        mock_token_response = MagicMock()
        mock_token_response.status_code = 401
        mock_token_response.text = 'Unauthorized' # Add text for error logging in the client
        # Configure raise_for_status to raise an HTTPError
        mock_token_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized for url") 
        mock_post.return_value = mock_token_response
        
        client = OpenverseClient()
        token = client._get_auth_token() # Changed method call
        
        assert token is None # Assert that token is None on error
