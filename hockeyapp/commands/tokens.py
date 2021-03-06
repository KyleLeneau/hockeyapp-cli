import click
import requests
import json
from hockeyapp.cli import pass_context

# URL for all the commands here
base_url = 'https://rink.hockeyapp.net/api/2/auth_tokens'

# Tokens Rights map
avail_rights = {'F': 0, 'U': 1, 'R': 2, 'UR': 3}


def validate_username(ctx, param, value):
    if value is None or len(value) == 0:
        raise click.BadParameter('Username needs to be specified')
    else:
        return value


@click.group(short_help='Create and retrieve HockeyApp Tokens for the current logged in user.')
@click.option('-u', '--username', help='Name of user to login as.', type=click.STRING, callback=validate_username)
@click.option('-p', '--password', help='Password for the user to login as.', prompt=True, hide_input=True)
@pass_context
def cli(ctx, username, password):
    ctx.username = username
    ctx.password = password


@cli.command(short_help='Lists all API tokens for the logged user.')
@pass_context
def list(ctx):
    """Gets a users available tokens."""
    req = requests.get(base_url, auth=(ctx.username, ctx.password))
    ctx.output_json(req.json())


@cli.command(short_help='Creates a new token.')
@click.option('-r', '--rights',
              help='Rights for the new token (F)ull Access, (U)pload Only, (R)ead Only, (UR)Upload & Release',
              type=click.Choice(['F', 'U', 'R', 'UR']))
@click.option('-n', '--name', help='(optional) Name for the new token.', type=click.STRING)
@pass_context
def create(ctx, rights, name):
    """Creates a new access token for the user"""
    data = {
        'rights': avail_rights[rights.upper()],
        'name': name
    }
    req = requests.post(base_url, auth=(ctx.username, ctx.password), data=data)
    ctx.output_json(req.json())
