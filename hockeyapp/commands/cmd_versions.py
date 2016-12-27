import click
import requests
import json
import urllib

from hockeyapp.cli import pass_context
from hockeyapp.util import *

@click.group(short_help='Information about HockeyApp Versions')
@pass_context
def cli(ctx):
    x = encode("foo")
    pass

@cli.command(short_help='Gets the list of versions for a given app.')
@token_option
@app_id_option
@pass_context
def list(ctx, token, app):
    """Gets the list of app versions for an App."""
    url = "https://rink.hockeyapp.net/api/2/apps/{}/app_versions"\
        .format(encode(app))
    headers = {
        'X-HockeyAppToken': token
    }
    req = requests.get(url, headers=headers)
    ctx.log(json.dumps(req.json(), indent=2))