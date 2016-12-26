import click
from hockeyapp.cli import pass_context
import requests
import json

def validate_hockeyapp_token(ctx, param, value):
    # ctx.vlog('Validating %s %s', param, value)
    if value is None or len(value) == 0:
        raise click.BadParameter('HockeyApp token needs to be specified')
    else:
        return value

@click.command('list_apps', short_help='Gets the list of apps the token has access to.')
@click.option('--token', envvar='HOCKEYAPP_TOKEN', type=click.STRING, callback=validate_hockeyapp_token)
@pass_context
def cli(ctx, token):
    """Gets the list of apps for the HockeyApp Token."""
    url = 'https://rink.hockeyapp.net/api/2/apps'
    headers = {
        'X-HockeyAppToken': token
    }
    req = requests.get(url, headers=headers)
    ctx.log(json.dumps(req.json(), indent=2))