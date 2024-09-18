
# mtl-tunedglobal

`mtl-tunedglobal` is an exerimental command-line interface (CLI) tool to interact with the Tuned Global API. It allows users to search for songs using the services API and retrieve podcasts using the metadata API.

## Features

- **Search Songs**: Search for songs by name using the Tuned Global services API.
- **Get All Podcasts**: Retrieve all podcasts using the Tuned Global metadata API.


## Installation

To install the dependencies, you can use Poetry:

```bash
poetry install
```

## Usage

This package provides two main CLI groups: `services` and `metadata`.

### Search for a Song

To search for a song, use the `services search-song` command and provide the song name:

```bash
poetry run app services search-song "Imagine"
```

### Get All Podcasts

To retrieve all podcasts, use the `metadata get-all-podcasts` command:

```bash
poetry run app metadata get-all-podcasts
```

## Project Structure

- **TunedGlobalClient**: Base class that handles API requests.
- **TunedGlobalMetadataClient**: Class that interacts with the metadata API.
- **TunedGlobalServicesClient**: Class that interacts with the services API.
- **CLI**: Command-line interface using `click` for interaction.

## Environment Variables

The API requires a `StoreId` which is your API key. You can set this in your environment or use a `.env` file.

```bash
export TUNEDGLOBAL_API_KEY="your_api_key"
```

Or create a `.env` file with the following content:

```bash
TUNEDGLOBAL_API_KEY=your_api_key
```

## Tests

To run test use this command
```bash
poetry run pytest
```

## License

This project is licensed under the MIT License.
