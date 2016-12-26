import click
from hockeyapp.cli import pass_context
import requests
import json
import urllib

def encode(s):
    return urllib.quote(s)

def validate_hockeyapp_token(ctx, param, value):
    # ctx.vlog('Validating %s %s', param, value)
    if value is None or len(value) == 0:
        raise click.BadParameter('HockeyApp token needs to be specified')
    else:
        return value

def validate_app_id(ctx, param, value):
    # ctx.vlog('Validating %s %s', param, value)
    if value is None or len(value) == 0:
        raise click.BadParameter('HockeyApp App Id needs to be specified')
    else:
        return value

@click.command('list_versions', short_help='Gets the list of versions for a given app.')
@click.option('--token', envvar='HOCKEYAPP_TOKEN', type=click.STRING, callback=validate_hockeyapp_token)
@click.option('--app', type=click.STRING, callback=validate_app_id)
@pass_context
def cli(ctx, token, app):
    """Gets the list of app versions for an App."""
    url = "https://rink.hockeyapp.net/api/2/apps/{}/app_versions"\
        .format(encode(app))
    headers = {
        'X-HockeyAppToken': token
    }
    req = requests.get(url, headers=headers)
    ctx.log(json.dumps(req.json(), indent=2))