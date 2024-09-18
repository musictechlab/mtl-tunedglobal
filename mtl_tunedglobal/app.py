import click
from mtl_tunedglobal.client import TunedGlobalServicesClient, TunedGlobalMetadataClient


@click.group()
def cli():
    """Tuned Global CLI."""
    pass


# Group for services-related commands
@click.group()
def services():
    """Commands related to Tuned Global Services API."""
    pass


# Group for metadata-related commands
@click.group()
def metadata():
    """Commands related to Tuned Global Metadata API."""
    pass


# Command under services group to search for a song
@services.command()
@click.argument('song_name')
def search_song(song_name):
    """Search for a song by name using TunedGlobalServicesClient."""
    client = TunedGlobalServicesClient()
    result = client.search_song(song_name)
    click.echo(result)


# Command under metadata group to get all podcasts
@metadata.command()
def get_all_podcasts():
    """Get all podcasts using TunedGlobalMetadataClient."""
    client = TunedGlobalMetadataClient()
    result = client.get_all_podcasts(offset=1, count=5)
    click.echo(result)


# Add the services and metadata commands to the main cli group
cli.add_command(services)
cli.add_command(metadata)

if __name__ == "__main__":
    cli()