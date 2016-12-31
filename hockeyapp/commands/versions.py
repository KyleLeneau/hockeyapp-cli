import click

from hockeyapp.cli import pass_context
from hockeyapp.util import *
from api import *


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
@click.option('--recent', is_flag=True, help='Only return the most recent version.')
@pass_context
def list(ctx, include_build_urls, recent):
    path = '/apps/{}/app_versions'.format(encode(ctx.app_id))
    data = {}
    if include_build_urls:
        data['include_build_urls'] = 'true'

    response = APIRequest(ctx.token, log=ctx.vlog).get(path, data)

    output = response['app_versions']
    if recent:
        # TODO: should order them first?
        output = output[0]

    ctx.output_json(output)


@cli.command(short_help='Get statistics about downloads, installs, and crashes for all versions.')
@click.option('--recent', is_flag=True, help='Only return the most recent version.')
@pass_context
def statistics(ctx, recent):
    path = '/apps/{}/statistics'.format(encode(ctx.app_id))
    response = APIRequest(ctx.token, log=ctx.vlog).get(path)

    output = response['app_versions']
    if recent:
        # TODO: should order them first?
        output = output[0]

    ctx.output_json(output)


@cli.command(short_help='Get App Source Information about a specific version.')
@version_id_option()
@pass_context
def sources(ctx, version):
    path = '/apps/{}/app_versions/{}/app_sources'.format(encode(ctx.app_id), encode(version))
    response = APIRequest(ctx.token, log=ctx.vlog).get(path)
    ctx.output_json(response['app_sources'])


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
