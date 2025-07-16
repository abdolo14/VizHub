import pytest
from unittest.mock import Mock, patch
from app import app
from data_processor import DataProcessor

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_github():
    with patch('app.github') as mock:
        yield mock

@pytest.fixture
def mock_db():
    with patch('app.Database') as mock:
        instance = Mock()
        mock.return_value.__enter__.return_value = instance
        yield instance

def test_get_repository(client, mock_github, mock_db):
    # Mock data
    mock_repo_data = {
        'id': 12345,
        'name': 'test-repo',
        'owner': {'login': 'test-user'},
        'stargazers_count': 100,
        'forks_count': 50,
        'created_at': '2023-01-01T00:00:00Z',
        'updated_at': '2023-07-01T00:00:00Z'
    }
    mock_github.get_repository_info.return_value = mock_repo_data
    mock_db.store_repository.return_value = 1

    # Make request
    response = client.get('/api/repository/test-user/test-repo')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['github_id'] == 12345
    assert data['name'] == 'test-repo'
    assert data['owner'] == 'test-user'
    assert data['stars'] == 100
    assert data['forks'] == 50

def test_get_contributors(client, mock_github, mock_db):
    mock_contrib_data = [
        {'login': 'user1', 'contributions': 50},
        {'login': 'user2', 'contributions': 30}
    ]
    mock_github.get_contributors.return_value = mock_contrib_data
    mock_github.get_repository_info.return_value = {'id': 12345}
    mock_db.store_repository.return_value = 1

    response = client.get('/api/contributors/test-user/test-repo')
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['github_username'] == 'user1'
    assert data[0]['contributions'] == 50

def test_error_handling(client, mock_github):
    mock_github.get_repository_info.side_effect = Exception('API Error')
    
    response = client.get('/api/repository/test-user/test-repo')
    assert response.status_code == 500
    
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'API Error'
    assert data['endpoint'] == '/api/repository/test-user/test-repo'
