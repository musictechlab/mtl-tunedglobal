from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def search_song():
    # API endpoint
    url = "https://api-delivery-connect.tunedglobal.com/api/v5/search/master/songs"

    # Extract query parameter for song name
    song_name = request.args.get('name', 'hello')

    # Set up headers
    headers = {
        "Accept": "application/json",
        "StoreId": os.getenv("TUNEDGLOBAL_API_KEY")
    }

    # Set up query parameters
    params = {
        "filter.name": song_name
    }

    # Make the GET request to the external API
    response = requests.get(url, headers=headers, params=params)

    # Return the JSON response
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)


# curl -X GET --header "Accept: application/json" --header "StoreId: qUistRalaSToNfi" "https://api-delivery-connect.tunedglobal.com/api/v5/search/master/songs?filter.name=hello"

# curl -X GET --header "Accept: application/json" --header "StoreId: qUistRalaSToNfi" "https://api-metadata-connect.tunedglobal.com/api/v5/search/master/songs?filter.name=hello"

    
    