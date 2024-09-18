import requests
import os

class TunedGlobalClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key or os.getenv("TUNEDGLOBAL_API_KEY")
    
    def _get_headers(self):
        return {
            "Accept": "application/json",
            "StoreId": self.api_key
        }
    
    def _make_get_request(self, endpoint, params=None):
        url = self.base_url + endpoint
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "response": response.json()}


class TunedGlobalMetadataClient(TunedGlobalClient):
    def __init__(self, api_key=None):
        super().__init__(base_url="https://api-metadata-connect.tunedglobal.com", api_key=api_key)

    def get_all_podcasts(self, offset=1, count=10):
        """
        Retrieve all podcasts from the metadata API.

        :param offset: The first row in the result set. Default is 1.
        :param count: The number of rows to return. Default is 10.
        :return: JSON response containing the podcast data.
        """
        endpoint = "/api/v2.3/podcasts/all"
        params = {
            "offset": offset,
            "count": count
        }
        return self._make_get_request(endpoint, params=params)


class TunedGlobalServicesClient(TunedGlobalClient):
    def __init__(self, api_key=None):
        super().__init__(base_url="https://api-delivery-connect.tunedglobal.com", api_key=api_key)

    def search_song(self, song_name="hello"):
        """
        Search for songs in the services API.

        :param song_name: The name of the song to search for. Default is 'hello'.
        :return: JSON response containing the song data.
        """
        endpoint = "/api/v5/search/master/songs"
        params = {
            "filter.name": song_name
        }
        print (params)
        return self._make_get_request(endpoint, params=params)
