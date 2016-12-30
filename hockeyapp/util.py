import click
import urllib


def encode(s):
    return urllib.quote(s)

def token_option(func):
    """Get a decorator for easy HockeyApp token input"""

    def callback(ctx, param, value):
        if value is None or len(value) == 0:
            raise click.BadParameter('HockeyApp token needs to be specified')
        else:
            return value

    return click.option('-t', '--token',
                        envvar='HOCKEYAPP_TOKEN',
                        type=click.STRING,
                        help='Specify the HockeyApp Token (can also set HOCKEYAPP_TOKEN env var).',
                        callback=callback)(func)

def app_id_option(func):
    """Get a decorator for App ID input"""

    def callback(ctx, param, value):
        if value is None or len(value) == 0:
            raise click.BadParameter('An App Id needs to be specified')
        else:
            return value

    return click.option('-a', '--app',
                        type=click.STRING,
                        help='Specify the HockeyApp App Id.',
                        callback=callback)(func)
