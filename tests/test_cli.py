import pytest
from click.testing import CliRunner
from unittest.mock import patch, Mock
from mtl_tunedglobal import cli  # Import the CLI group

@pytest.fixture
def runner():
    return CliRunner()

def test_search_song_command(runner):
    # Mock the TunedGlobalServicesClient's search_song method
    with patch('mtl_tunedglobal.client.TunedGlobalServicesClient.search_song') as mock_search_song:
        mock_search_song.return_value = {
            "data": [{"song_name": "Imagine", "artist": "John Lennon"}]
        }
        
        # Since search_song is now under the 'services' group, we use 'services search-song'
        result = runner.invoke(cli, ['services', 'search-song', 'Imagine'])
        
        # Assert the CLI command runs successfully
        assert result.exit_code == 0
        assert "Imagine" in result.output
        mock_search_song.assert_called_once_with("Imagine")

def test_get_all_podcasts_command(runner):
    # Mock the TunedGlobalMetadataClient's get_all_podcasts method
    with patch('mtl_tunedglobal.client.TunedGlobalMetadataClient.get_all_podcasts') as mock_get_all_podcasts:
        mock_get_all_podcasts.return_value = {
            "Results": [{"Title": "Sample Podcast"}],
            "Total": 1
        }
        
        # Since get_all_podcasts is now under the 'metadata' group, we use 'metadata get-all-podcasts'
        result = runner.invoke(cli, ['metadata', 'get-all-podcasts'])
        
        # Assert the CLI command runs successfully
        assert result.exit_code == 0
        assert "Sample Podcast" in result.output
        mock_get_all_podcasts.assert_called_once_with(offset=1, count=5)