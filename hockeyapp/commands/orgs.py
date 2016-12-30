import click

from hockeyapp.cli import pass_context
from hockeyapp.util import *
from api import *


def org_id_option(func):
    """Get a decorator for Organization ID input"""

    def callback(ctx, param, value):
        if value is None or len(value) == 0:
            raise click.BadParameter('An Organization Id needs to be specified')
        else:
            return value

    return click.option('-o', '--org',
                        type=click.STRING,
                        help='Specify the Organization Id.',
                        callback=callback)(func)


@click.group(short_help='Lets you query the organizations for an account.')
@token_option
@pass_context
def cli(ctx, token):
    ctx.token = token


@cli.command(short_help='List all organizations for the authenticated user.')
@pass_context
def list(ctx):
    response = APIRequest(ctx.token, log=ctx.vlog).get('/organizations')
    ctx.output_json(response)


@cli.command(short_help='Upload an .ipa, .apk, or .zip file to create a new app.')
@org_id_option
@pass_context
def teams(ctx, org):
    path = '/organizations/{}/teams'.format(encode(org))
    response = APIRequest(ctx.token, log=ctx.vlog).get(path)
    ctx.output_json(response)
