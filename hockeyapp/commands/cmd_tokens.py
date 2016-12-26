import click
from hockeyapp.cli import pass_context
import requests
import json

def validate_username(ctx, param, value):
    if value is None or len(value) == 0:
        raise click.BadParameter('Username needs to be specified')
    else:
        return value

@click.command('tokens', short_help='Gets the list of tokens for a user.')
@click.option('--username', type=click.STRING, callback=validate_username)
@click.option('--password', prompt=True, hide_input=True)
@pass_context
def cli(ctx, username, password):
    """Gets a users available tokens."""
    ctx.vlog('Tokens for %s:%s', username, password)
    req = requests.get('https://rink.hockeyapp.net/api/2/auth_tokens', auth=(username, password))
    ctx.log(json.dumps(req.json(), indent=2))