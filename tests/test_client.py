import pytest
from unittest.mock import patch, Mock
from mtl_tunedglobal.client import TunedGlobalClient, TunedGlobalMetadataClient, TunedGlobalServicesClient

@pytest.fixture
def client():
    return TunedGlobalClient(base_url="https://api-delivery-connect.tunedglobal.com", store_id="mocked_store_id")

@pytest.fixture
def metadata_client():
    return TunedGlobalMetadataClient(store_id="mocked_store_id")

@pytest.fixture
def services_client():
    return TunedGlobalServicesClient(store_id="mocked_store_id")

def test_login_success(client):
    with patch('mtl_tunedglobal.client.requests.post') as mock_post:
        # Mock a successful login response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "mocked_token"}
        mock_post.return_value = mock_response

        # Perform login
        client.login(username="testuser", password="testpassword")

        # Assertions
        mock_post.assert_called_once_with(
            "https://api-authentication-connect.tunedglobal.com/oauth2/token",
            headers={
                'StoreID': 'mocked_store_id',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'grant_type': 'password',
                'username': 'testuser',
                'password': 'testpassword'
            }
        )
        assert client.token == "mocked_token"

def test_login_failure(client):
    with patch('mtl_tunedglobal.client.requests.post') as mock_post:
        # Mock a failed login response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "invalid_grant"}
        mock_post.return_value = mock_response

        # Perform login and expect a system exit due to failure
        with pytest.raises(SystemExit):
            client.login(username="testuser", password="wrongpassword")

        # Assertions
        mock_post.assert_called_once_with(
            "https://api-authentication-connect.tunedglobal.com/oauth2/token",
            headers={
                'StoreID': 'mocked_store_id',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'grant_type': 'password',
                'username': 'testuser',
                'password': 'wrongpassword'
            }
        )

def test_search_song(services_client):
    with patch('mtl_tunedglobal.client.requests.get') as mock_get:
        # Mock a successful search song response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"song_name": "Imagine", "artist": "John Lennon"}]
        }
        mock_get.return_value = mock_response

        # Set a mock token
        services_client.token = "mocked_token"

        # Perform song search
        result = services_client.search_song(song_name="Imagine")

        # Assertions
        mock_get.assert_called_once_with(
            "https://api-delivery-connect.tunedglobal.com/api/v5/search/master/songs",
            headers={
                "Accept": "application/json",
                "StoreId": "mocked_store_id",
                "Authorization": "Bearer mocked_token"
            },
            params={"filter.name": "Imagine"}
        )
        assert result == {"data": [{"song_name": "Imagine", "artist": "John Lennon"}]}

def test_get_all_podcasts(metadata_client):
    with patch('mtl_tunedglobal.client.requests.get') as mock_get:
        # Mock a successful get all podcasts response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Results": [{"Title": "Sample Podcast"}],
            "Total": 1
        }
        mock_get.return_value = mock_response

        # Set a mock token
        metadata_client.token = "mocked_token"

        # Perform get all podcasts
        result = metadata_client.get_all_podcasts(offset=1, count=5)

        # Assertions
        mock_get.assert_called_once_with(
            "https://api-metadata-connect.tunedglobal.com/api/v2.3/podcasts/all",
            headers={
                "Accept": "application/json",
                "StoreId": "mocked_store_id",
                "Authorization": "Bearer mocked_token"
            },
            params={"offset": 1, "count": 5}
        )
        assert result == {
            "Results": [{"Title": "Sample Podcast"}],
            "Total": 1
        }