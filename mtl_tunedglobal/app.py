import click
import os

TOKEN_FILE = "token.txt"

@click.group()
@click.pass_context
def cli(ctx):
    """Tuned Global CLI."""
    from .client import TunedGlobalClient  # Import here to avoid circular imports

    client = TunedGlobalClient(base_url="https://api-delivery-connect.tunedglobal.com")
    
    # Load token from file if it exists
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r', encoding='utf-8') as file:
            client.token = file.read().strip()
    
    ctx.obj = client

@cli.command()
@click.argument('username')
@click.argument('password')
@click.pass_obj
def login(client, username, password):
    """Authenticate and store the bearer token for future use."""
    client.login(username, password)
    
    # Save the token to a file
    with open(TOKEN_FILE, 'w', encoding='utf-8') as file:
        file.write(client.token)
    
    click.echo(f"Logged in successfully.")
    

# Group for services-related commands
@cli.group()
@click.pass_obj
def services(client):
    """Commands related to Tuned Global Services API."""
    pass

# Group for metadata-related commands
@cli.group()
@click.pass_obj
def metadata(client):
    """Commands related to Tuned Global Metadata API."""
    pass

# Command under services group to search for a song
@services.command()
@click.argument('song_name')
@click.pass_obj
def search_song(client, song_name):
    """Search for a song by name using TunedGlobalServicesClient."""
    if not client.token:
        raise click.UsageError("You must login first before using this command.")
    
    from .client import TunedGlobalServicesClient  # Import here to avoid circular imports
    
    service_client = TunedGlobalServicesClient(api_key=client.api_key)
    service_client.token = client.token  # Share the token
    result = service_client.search_song(song_name)
    click.echo(result)

# Command under metadata group to get all podcasts
@metadata.command()
@click.pass_obj
def get_all_podcasts(client):
    """Get all podcasts using TunedGlobalMetadataClient."""
    if not client.token:
        raise click.UsageError("You must login first before using this command.")
    
    from .client import TunedGlobalMetadataClient  # Import here to avoid circular imports
    
    metadata_client = TunedGlobalMetadataClient(api_key=client.api_key)
    metadata_client.token = client.token  # Share the token
    result = metadata_client.get_all_podcasts(offset=1, count=5)
    click.echo(result)

if __name__ == "__main__":
    cli()