# client.py
from dotenv import load_dotenv
import requests
import os

load_dotenv()


class TunedGlobalClient:
    def __init__(self, base_url, store_id=None):
        self.base_url = base_url
        self.store_id = store_id or os.getenv("TUNEDGLOBAL_STORE_ID")
        self.token = None

    def _get_headers(self):
        if not self.token:
            raise ValueError("Authentication token is missing. Please login first.")
        headers = {
            "Accept": "application/json",
            "StoreId": self.store_id,
            "Authorization": f"Bearer {self.token}"
        }
        return headers
    
    def _make_get_request(self, endpoint, params=None):
        url = self.base_url + endpoint
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "response": response.json()}

    def login(self, username, password):
        """
        Authenticate to get bearer token and store it in the client.
        """
        endpoint_auth = "https://api-authentication-connect.tunedglobal.com/oauth2/token"
        content_type = "application/x-www-form-urlencoded"
        
        auth_response = requests.post(
            endpoint_auth,
            headers={
                'StoreID': self.store_id,
                'Content-Type': content_type
            },
            data={
                'grant_type': 'password',
                'username': username,
                'password': password
            }
        )

        if auth_response.status_code == 200:
            self.token = auth_response.json().get('access_token')
            print(f"Token: {self.token} | Authentication successful.")
        else:
            print(f"Authentication failed with status code: {auth_response.status_code}.")
            print(auth_response.text)
            exit(1)

class TunedGlobalMetadataClient(TunedGlobalClient):
    def __init__(self, store_id=None):
        super().__init__(base_url="https://api-metadata-connect.tunedglobal.com", store_id=store_id)

    def get_all_podcasts(self, offset=1, count=10):
        endpoint = "/api/v2.3/podcasts/all"
        params = {
            "offset": offset,
            "count": count
        }
        return self._make_get_request(endpoint, params=params)

class TunedGlobalServicesClient(TunedGlobalClient):
    def __init__(self, store_id=None):
        super().__init__(base_url="https://api-delivery-connect.tunedglobal.com", store_id=store_id)

    def search_song(self, song_name="hello"):
        endpoint = "/api/v5/search/master/songs"
        params = {
            "filter.name": song_name
        }
        return self._make_get_request(endpoint, params=params)