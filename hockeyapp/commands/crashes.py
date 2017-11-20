import click

from hockeyapp.cli import pass_context
from hockeyapp.util import *
from api import *

def query_callback(ctx, param, value):
    if value is None or len(value) == 0:
        raise click.BadParameter('A Query needs to be specified')
    else:
        return value

@click.group(short_help='API lets you list crash groups, list crashes, download logs and description, getting a '
                        'histogram, or post custom crash reports.')
@token_option
@pass_context
def cli(ctx, token):
    ctx.token = token

@cli.command(short_help='List all crash groups for an app or version.')
@app_id_option()
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
@app_id_option()
@crash_group_option()
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
@app_id_option()
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

@cli.command(short_help='Get a histogram of the number of crashes between two given dates for an App, '
                        'Version or Crash Group.')
@app_id_option()
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
    ctx.output_json(response['histogram'])

@cli.command(short_help='Search for crashes by query from an App or Version.')
@app_id_option()
@version_id_option(required=False)
@click.option('-q', '--query',
              type=click.STRING,
              help='Search to use for looking for crashes.',
              callback=query_callback)
@pass_context
def search(ctx, app, version, query):
    path = '/apps/{}/crashes/search'.format(encode(app))
    if version is not None and len(version) > 0:
        path = '/apps/{}/app_versions/{}/crashes/search'.format(encode(app), encode(version))

    data = {
        'query': encode(query)
    }

    response = APIRequest(ctx.token, log=ctx.vlog).get(path, data=data)
    ctx.output_json(response)

@cli.command(short_help='Search for crashes by query from an App or Version.')
@app_id_option()
@version_id_option(required=False)
@click.option('-q', '--query',
              type=click.STRING,
              help='Search to use for looking for crash groups.',
              callback=query_callback)
@pass_context
def search_groups(ctx, app, version, query):
    path = '/apps/{}/crash_reasons/search'.format(encode(app))
    if version is not None and len(version) > 0:
        path = '/apps/{}/app_versions/{}/crash_reasons/search'.format(encode(app), encode(version))

    data = {
        'query': encode(query)
    }

    response = APIRequest(ctx.token, log=ctx.vlog).get(path, data=data)
    ctx.output_json(response)

@cli.command(short_help='Set the status of a crash group or assign a ticket URL.')
@app_id_option()
@crash_group_option()
@click.option('-s', '--status',
              type=click.Choice(['O', 'R', 'I']),
              help='optional, et the status of the crash group (O)pen, (R)esolved, or (I)gnored.')
@click.option('-t', '--ticket-url',
              type=click.STRING,
              help='optional, set to URL for a ticket in your bug tracker.')
@pass_context
def update(ctx, app, group, status, ticket_url):
    path = '/apps/{}/crash_reasons/{}'.format(encode(app), encode(group))
    data = {}

    if status is not None and len(status) > 0:
        if status == 'O':
            data['status'] = 0
        elif status == 'R':
            data['status'] = 1
        elif status == 'I':
            data['status'] = 2

    if ticket_url is not None and len(ticket_url) > 0:
        data['ticket_url'] = ticket_url

    response = APIRequest(ctx.token, log=ctx.vlog).post(path, data=data)
    ctx.output_json(response)

@cli.command(short_help='Set the status of a crash group or assign a ticket URL.')
@app_id_option()
@crash_group_option()
@click.option('-t', '--text',
              type=click.STRING,
              help='optional, the new annotation text.')
@click.option('-c', '--clear',
              help='Clear the annotation text.',
              is_flag=True)
@pass_context
def annotate(ctx, app, group, text, clear):
    path = '/apps/{}/crash_reasons/{}/crash_annotations'.format(encode(app), encode(group))

    if clear:
        response = APIRequest(ctx.token, log=ctx.vlog).delete(path)
        ctx.output_json(response)
    elif text is not None and len(text) > 0:
        data = {'text': text}
        response = APIRequest(ctx.token, log=ctx.vlog).post(path, data=data)
        ctx.output_json(response)
    else:
        response = APIRequest(ctx.token, log=ctx.vlog).get(path)
        ctx.output_json(response)


# TODO: Add Custom crashes CLI command
