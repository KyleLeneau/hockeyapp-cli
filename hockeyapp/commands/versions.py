import click
import requests
import json

from hockeyapp.cli import pass_context
from hockeyapp.util import *


# URL for all the commands here
base_url = 'https://rink.hockeyapp.net/api/2/apps'


@click.group(short_help='This Developer API for versions lets you list versions of an app, upload, create, or update a '
                        'version, or delete a single or delete multiple versions. All endpoints require '
                        'authentication with an API token.')
@pass_context
def cli(ctx):
    pass


@cli.command(short_help='List all versions of an app. The endpoint returns all versions for developer and members, '
                        'but only released versions for testers.')
@token_option
@app_id_option
@pass_context
def list(ctx, token, app):
    url = "{}/{}/app_versions"\
        .format(base_url, encode(app))
    headers = {
        'X-HockeyAppToken': token
    }
    req = requests.get(url, headers=headers)
    ctx.log(json.dumps(req.json(), indent=2))


@cli.command(short_help='Get statistics about downloads, installs, and crashes for all versions.')
@token_option
@app_id_option
@pass_context
def statistics(ctx, token, app):
    url = "{}/{}/statistics"\
        .format(base_url, encode(app))
    headers = {
        'X-HockeyAppToken': token
    }
    req = requests.get(url, headers=headers)
    ctx.log(json.dumps(req.json(), indent=2))


@cli.command(short_help='Upload an .ipa, .apk, .appx, or .zip file to create a new version for your app.')
@token_option
@pass_context
def upload(ctx, token):
    pass


@cli.command(short_help='Create a version without uploading files.')
@token_option
@pass_context
def create(ctx, token):
    pass


@cli.command(short_help='Update the attributes of an existing version.')
@token_option
@pass_context
def update(ctx, token):
    pass


@cli.command(short_help='Delete a single version.')
@token_option
@pass_context
def delete(ctx, token):
    pass


@cli.command(short_help='Delete multiple versions with one request.')
@token_option
@pass_context
def delete_batch(ctx, token):
    pass