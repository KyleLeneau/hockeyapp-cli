import click
from hockeyapp.cli import pass_context
import requests
import json

from hockeyapp.util import *

@click.group(short_help='Information about HockeyApp Apps')
@pass_context
def cli(ctx):
    pass

@cli.command(short_help='Gets the list of apps the token has access to.')
@token_option
@pass_context
def list(ctx, token):
    url = 'https://rink.hockeyapp.net/api/2/apps'
    headers = {
        'X-HockeyAppToken': token
    }
    req = requests.get(url, headers=headers)
    ctx.log(json.dumps(req.json(), indent=2))