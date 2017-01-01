import click

from hockeyapp.cli import pass_context
from hockeyapp.util import *
from api import *

# Define roles constant
user_roles = {'O': 0, 'D': 1, 'M': 2, 'T': 3}


def team_id_callback(ctx, param, value):
    if value is None or value == 0:
        raise click.BadParameter('A Team ID needs to be specified')
    else:
        return value


def email_callback(ctx, param, value):
    if not string_has_value(value):
        raise click.BadParameter('An Email Address needs to be specified')
    else:
        return value


def user_id_callback(ctx, param, value):
    if value is None or value == 0:
        raise click.BadParameter('A User Id needs to be specified')
    else:
        return value


def app_secret_callback(ctx, param, value):
    if not string_has_value(value):
        raise click.BadParameter('An App Secret must be specified')
    else:
        return value


@click.group(short_help='Manage users for accounts and apps.')
@token_option
@pass_context
def cli(ctx, token):
    ctx.token = token


@cli.command(short_help='List Users of App.')
@app_id_option()
@pass_context
def list(ctx, app):
    path = '/apps/{}/app_users'.format(encode(app))
    response = APIRequest(ctx.token, log=ctx.vlog).get(path)
    ctx.output_json(response)


@cli.command(short_help='Invite User to App.')
@app_id_option()
@click.option('-e', '--email',
              help='Email of the new user.',
              type=click.STRING,
              callback=email_callback)
@click.option('-f', '--first-name',
              help='optional, First name of the new user.',
              type=click.STRING)
@click.option('-l', '--last-name',
              help='optional, Last name of the new user.',
              type=click.STRING)
@click.option('-m', '--message',
              help='optional, Text message which is added to the invitation email.',
              type=click.STRING)
@click.option('-r', '--role',
              help='optional, Role for new user (D)eveloper, (M)ember, or (T)ester.',
              type=click.Choice(['D', 'M', 'T']))
@click.option('-t', '--tags',
              help='optional, Comma-separated list of tags for this user.',
              type=click.STRING)
@pass_context
def invite(ctx, app, email, first_name, last_name, message, role, tags):
    path = '/apps/{}/app_users'.format(encode(app))
    data = {
        'email': email
    }

    if string_has_value(first_name):
        data['first_name'] = first_name

    if string_has_value(last_name):
        data['last_name'] = last_name

    if string_has_value(message):
        data['message'] = message

    if string_has_value(role):
        data['role'] = user_roles[role]

    if string_has_value(tags):
        data['tags'] = tags

    response = APIRequest(ctx.token, log=ctx.vlog).post(path, data=data)
    ctx.output_json(response)


@cli.command(short_help='Check Membership of App (for user).')
@app_id_option()
@click.option('-e', '--email',
              help='Email of the new user.',
              type=click.STRING,
              callback=email_callback)
@click.option('-s', '--secret',
              help='Secret for the App.',
              type=click.STRING,
              callback=app_secret_callback)
@pass_context
def check(ctx, app, email, secret):
    path = '/apps/{}/app_users'.format(encode(app))
    data = {
        'email': email,
        'secret': secret
    }

    response = APIRequest(ctx.token, log=ctx.vlog).get(path, data=data)
    ctx.output_json(response)


@cli.command(short_help='Update User.')
@app_id_option()
@click.option('-u', '--user',
              help='User Id to remove',
              type=click.INT,
              callback=user_id_callback)
@click.option('-r', '--role',
              help='optional, Role for new user (D)eveloper, (M)ember, or (T)ester.',
              type=click.Choice(['D', 'M', 'T']))
@click.option('-t', '--tags',
              help='optional, Comma-separated list of tags for this user.',
              type=click.STRING)
@pass_context
def update(ctx, app, user, role, tags):
    path = '/apps/{}/app_users/{}'.format(encode(app), user)
    data = {}

    if string_has_value(role):
        data['role'] = user_roles[role]

    if string_has_value(tags):
        data['tags'] = tags

    response = APIRequest(ctx.token, log=ctx.vlog).put(path, data=data)
    ctx.output_json(response)


@cli.command(short_help='Remove User from App.')
@app_id_option()
@click.option('-u', '--user',
              help='User Id to remove',
              type=click.INT,
              callback=user_id_callback)
@pass_context
def remove(ctx, app, user):
    path = '/apps/{}/app_users/{}'.format(encode(app), user)
    response = APIRequest(ctx.token, log=ctx.vlog).delete(path)
    ctx.output_json(response)
