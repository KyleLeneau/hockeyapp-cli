import click
import requests

from hockeyapp.cli import pass_context
from hockeyapp.util import *

# URL for all the commands here
base_url = 'https://rink.hockeyapp.net/api/2/apps'

# Options for note types
notes_type = { 'Textile': 0, 'T': 0, 'Markdown': 1, 'M': 1 }


@click.group(short_help='API for apps that lets you list all apps in your account, '
                        'upload, create, or delete an app.')
@token_option
@pass_context
def cli(ctx, token):
    ctx.token = token


@cli.command(short_help='List all apps for the logged user, including owned apps, developer apps, '
                        'member apps, and tester apps.')
@pass_context
def list(ctx):
    url = 'https://rink.hockeyapp.net/api/2/apps'
    headers = {
        'X-HockeyAppToken': ctx.token
    }
    ctx.output_json(requests.get(url, headers=headers).json())


@cli.command(short_help='Upload an .ipa, .apk, or .zip file to create a new app.')
@pass_context
def upload(ctx):
    pass


@cli.command(short_help='Create a new app without uploading a file.')
@pass_context
def new(ctx, token):
    pass


@cli.command(short_help='Delete the app with the given App ID.')
@pass_context
def delete(ctx, token):
    pass


@cli.command(short_help='Configure settings of the app.')
@pass_context
def configure(ctx, token):
    pass
