import click

from hockeyapp.cli import pass_context
from hockeyapp.util import *
from api import *


@click.group(short_help='API lets you list crash groups, list crashes, download logs and description, getting a '
                        'histogram, or post custom crash reports.')
@token_option
@pass_context
def cli(ctx, token):
    ctx.token = token


@cli.command(short_help='List all crash groups for an app or version.')
@app_id_option
@version_id_option(required=False)
@page_option
@page_size_option
@click.option('-s', '--symbolicated',
              help='optional, use you only want crashes that have run through the symbolication process',
              is_flag=True)
@click.option('--sort',
              help='optional, sort by "date" (default), "class", "number_of_crashes", "last_crash_at"',
              type=click.Choice(['date', 'class', 'number_of_crashes', 'last_crash_at']))
@click.option('--order',
              help='optional, "asc" for ascending order (default) or "desc" for descending order',
              type=click.Choice(['asc', 'desc']))
@pass_context
def groups(ctx, app, version, page, page_size, symbolicated, sort, order):
    path = '/apps/{}/crash_reasons'.format(encode(app))
    if version is not None and len(version) > 0:
        path = '/apps/{}/app_versions/{}/crash_reasons'.format(encode(app), encode(version))

    data = {}

    if page is not None:
        data['page'] = page

    if page_size is not None:
        data['per_page'] = page_size

    if symbolicated:
        data['symbolicated'] = 1

    if sort is not None:
        data['sort'] = sort

    if order is not None:
        data['order'] = order

    response = APIRequest(ctx.token, log=ctx.vlog).get(path, data=data)
    ctx.output_json(response)


@cli.command(short_help='List all crashes of a crash group.')
@app_id_option
@crash_group_option
@page_option
@page_size_option
@pass_context
def reasons(ctx, app, group, page, page_size):
    path = '/apps/{}/crash_reasons/{}'.format(encode(app), encode(group))
    data = {}

    if page is not None:
        data['page'] = page

    if page_size is not None:
        data['per_page'] = page_size

    response = APIRequest(ctx.token, log=ctx.vlog).get(path, data=data)
    ctx.output_json(response)


@cli.command(short_help='Query a single crash log, its meta data, or the description.')
@app_id_option
@crash_id_option
@click.option('-f', '--form',
              help="required, set to \"log\" for the crash log, to \"json\" for the meta data, and to \"text\" for "
                   "the description",
              type=click.Choice(['log', 'json', 'text']),
              default='json')
@pass_context
def crash(ctx, app, crash, form):
    path = '/apps/{}/crashes/{}'.format(encode(app), encode(crash))
    data = {
        'format': form
    }

    response = APIRequest(ctx.token, log=ctx.vlog).get(path, data=data)
    ctx.output_json(response)


@cli.command(short_help='List all crashes of a crash group.')
@app_id_option
@version_id_option(required=False)
@crash_group_option(required=False)
@date_option('-s', '--start')
@date_option('-e', '--end')
@pass_context
def histogram(ctx, app, version, group, start, end):
    path = '/apps/{}/crashes/histogram'.format(encode(app))
    if version is not None and len(version) > 0:
        path = '/apps/{}/app_versions/{}/crashes/histogram'.format(encode(app), encode(version))

    if group is not None and len(group) > 0:
        path = '/apps/{}/crash_reasons/{}/histogram'.format(encode(app), encode(group))

    data = {
        'start_date': start,
        'end_date': end
    }

    response = APIRequest(ctx.token, log=ctx.vlog).get(path, data=data)
    ctx.output_json(response)


# Search crashes
# Search crash groups
# Update Group Status & Ticket
# Custom crashes
# anotations?

