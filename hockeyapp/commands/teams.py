import click

from hockeyapp.cli import pass_context
from hockeyapp.util import *
from api import *


def team_id_callback(ctx, param, value):
    if value is None or value == 0:
        raise click.BadParameter('A Team ID needs to be specified')
    else:
        return value


@click.group(short_help='Manage teams for accounts and apps.')
@token_option
@pass_context
def cli(ctx, token):
    ctx.token = token


@cli.command(short_help='List all teams.')
@app_id_option(required=False)
@page_option
@page_size_option
@pass_context
def list(ctx, app, page, page_size):
    path = '/teams'
    if app is not None and len(app) > 0:
        path = '/apps/{}/app_teams'.format(encode(app))

    data = {}

    if page is not None:
        data['page'] = page

    if page_size is not None:
        data['per_page'] = page_size

    response = APIRequest(ctx.token, log=ctx.vlog).get(path, data=data)
    ctx.output_json(response)


@cli.command(short_help='Add Team to App.')
@app_id_option()
@click.option('-t', '--team',
              help='required, specify the Team ID to add',
              type=click.INT,
              callback=team_id_callback)
@pass_context
def add(ctx, app, team):
    path = '/apps/{}/app_teams/{}'.format(encode(app), team)
    response = APIRequest(ctx.token, log=ctx.vlog).put(path)
    ctx.output_json(response)


@cli.command(short_help='Remove Team from App.')
@app_id_option()
@click.option('-t', '--team',
              help='required, specify the Team ID to add',
              type=click.INT,
              callback=team_id_callback)
@pass_context
def remove(ctx, app, team):
    path = '/apps/{}/app_teams/{}'.format(encode(app), team)
    response = APIRequest(ctx.token, log=ctx.vlog).delete(path)
    ctx.output_json(response)
