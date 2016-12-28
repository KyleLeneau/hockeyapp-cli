import click
import requests
import json

from hockeyapp.cli import pass_context
from hockeyapp.util import *


# URL for all the commands here
base_url = 'https://rink.hockeyapp.net/api/2/apps'

# Options for note types
notes_type = { 'Textile': 0, 'T': 0, 'Markdown': 1, 'M': 1 }


@click.group(short_help='This Developer API for apps lets you list all apps in your account, and upload, create, '
                        'or delete an app. All endpoints require authentication with an API token.')
@click.pass_context
def cli(ctx):
    pass


@cli.resultcallback()
def process_result(result):
    print(json.dumps(result.json(), indent=2))


@cli.command(short_help='List all apps for the logged user, including owned apps, developer apps, '
                        'member apps, and tester apps.')
@token_option
@pass_context
def list(ctx, token):
    url = 'https://rink.hockeyapp.net/api/2/apps'
    headers = {
        'X-HockeyAppToken': token
    }
    return requests.get(url, headers=headers)


@cli.command(short_help='Upload an .ipa, .apk, or .zip file to create a new app.')
@token_option
@pass_context
def upload(ctx, token):
    pass


@cli.command(short_help='Create a new app without uploading a file.')
@token_option
@pass_context
def new(ctx, token):
    pass


@cli.command(short_help='Delete the app with the given App ID.')
@token_option
@pass_context
def delete(ctx, token):
    pass


@cli.command(short_help='Configure settings of the app.')
@token_option
@pass_context
def configure(ctx, token):
    pass
