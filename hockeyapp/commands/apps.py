import click

from hockeyapp.cli import pass_context
from hockeyapp.util import *
from api import *


# Options for note types
notes_type = { 'Textile': 0, 'T': 0, 'Markdown': 1, 'M': 1 }

release_type = { 'Alpha': 2, 'Beta': 0, 'Store': 1, 'Enterprise': 3 }


def title_callback(ctx, param, value):
    if not string_has_value(value):
        raise click.BadParameter('An App Title needs to be specified')
    else:
        return value


def bundle_callback(ctx, param, value):
    if not string_has_value(value):
        raise click.BadParameter('A Bundle ID needs to be specified')
    else:
        return value


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
    response = APIRequest(ctx.token, log=ctx.vlog).get('/apps')
    ctx.output_json(response['apps'])


@cli.command(short_help='Upload an .ipa, .apk, or .zip file to create a new app.')
@pass_context
def upload(ctx):
    pass


@cli.command(short_help='Create a new app without uploading a file.')
@click.option('-t', '--title',
              type=click.STRING,
              help='required, the new apps name',
              callback=title_callback)
@click.option('-b', '--bundle',
              type=click.STRING,
              help='required, the bundle identifier on iOS or Mac OS X, the package name on Android, or the namespace '
                   'on Windows Phone',
              callback=bundle_callback)
@click.option('-p', '--platform',
              help='optional, the apps platform',
              type=click.Choice(['iOS', 'Android', 'Mac OS', 'Windows Phone', 'Custom']),
              default='iOS')
@click.option('-r', '--release-type',
              help='optional, set the release type of the app',
              type=click.Choice(['Alpha', 'Beta', 'Store', 'Enterprise']),
              default='Beta')
@click.option('-c', '--custom-type',
              type=click.STRING,
              help='optional, set to the custom release type string')
@click.option('-i', '--icon',
              help='optional, icon file with content type image/png, image/jpeg, or image image/gif')
@click.option('--public',
              help='optional, pass to enable the public download page (default is private)',
              is_flag=True)
@click.option('-o', '--owner',
              type=click.INT,
              help='optional, set to the ID of your organization')
@pass_context
def create(ctx, title, bundle, platfrom, release_type, custom_type, icon, public, owner):
    data = {}

    # response = APIRequest(ctx.token, log=ctx.vlog).post('/apps/new', data=data)
    # ctx.output_json(response)
    pass


@cli.command(short_help='Delete the app with the given App ID.')
@pass_context
def delete(ctx, token):
    pass


@cli.command(short_help='Configure settings of the app.')
@pass_context
def configure(ctx, token):
    pass

