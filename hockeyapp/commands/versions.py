import click
import requests
import json

from hockeyapp.cli import pass_context
from hockeyapp.util import *


# URL for all the commands here
base_url = 'https://rink.hockeyapp.net/api/2/apps'


@click.group(short_help='API for versions that lets you list versions of an app, upload, create, or update a '
                        'version, or delete a single or delete multiple versions.')
@token_option
@app_id_option
@pass_context
def cli(ctx, token, app):
    ctx.token = token
    ctx.app_id = app


@cli.command(short_help='List all versions of an app. The endpoint returns all versions for developer and members, '
                        'but only released versions for testers.')
@click.option('-b', '--include-build-urls', is_flag=True, help='Include the direct build URLs.')
@pass_context
def list(ctx, include_build_urls):
    url = "{}/{}/app_versions"\
        .format(base_url, encode(ctx.app_id))
    data = {}
    if include_build_urls:
        data['include_build_urls'] = 'true'
    headers = {
        'X-HockeyAppToken': ctx.token
    }
    req = requests.get(url, headers=headers, data=data)
    ctx.output_json(req.json())


@cli.command(short_help='Get statistics about downloads, installs, and crashes for all versions.')
@pass_context
def statistics(ctx):
    url = "{}/{}/statistics"\
        .format(base_url, encode(ctx.app_id))
    headers = {
        'X-HockeyAppToken': ctx.token
    }
    req = requests.get(url, headers=headers)
    ctx.output_json(req.json())


@cli.command(short_help='Upload an .ipa, .apk, .appx, or .zip file to create a new version for your app.')
@pass_context
def upload(ctx):
    pass


@cli.command(short_help='Create a version without uploading files.')
@pass_context
def create(ctx):
    pass


@cli.command(short_help='Update the attributes of an existing version.')
@pass_context
def update(ctx):
    pass


@cli.command(short_help='Delete a single version.')
@pass_context
def delete(ctx):
    pass


@cli.command(short_help='Delete multiple versions with one request.')
@pass_context
def delete_batch(ctx):
    pass
