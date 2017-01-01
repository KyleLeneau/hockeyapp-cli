import click
import urllib
import re


def encode(s):
    return urllib.quote(s)


def string_has_value(value):
    return value is not None and len(value) > 0


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


def app_id_option(required=True):
    """Get a decorator for App ID input"""

    def decorator(f):
        def callback(ctx, param, value):
            if required and (value is None or len(value) == 0):
                raise click.BadParameter('An App Id needs to be specified')
            else:
                return value

        return click.option('-a', '--app',
                            type=click.STRING,
                            help='Specify the HockeyApp App Id.',
                            callback=callback)(f)

    return decorator


def version_id_option(required=True):
    """Get a decorator for Version ID input"""

    def decorator(f):
        def callback(ctx, param, value):
            if required and (value is None or len(value) == 0):
                raise click.BadParameter('A Version Id needs to be specified')
            else:
                return value

        return click.option('-v', '--version',
                            type=click.STRING,
                            help='Specify the HockeyApp Version Id.',
                            callback=callback)(f)

    return decorator


def crash_group_option(required=True):
    """Get a decorator for Crash Group ID input"""

    def decorator(f):
        def callback(ctx, param, value):
            if required and (value is None or len(value) == 0):
                raise click.BadParameter('A Crash Group Id needs to be specified')
            else:
                return value

        return click.option('-g', '--group',
                            type=click.STRING,
                            help='Specify the Crash Group Id.',
                            callback=callback)(f)

    return decorator


def crash_id_option(func):
    """Get a decorator for Crash ID input"""

    def callback(ctx, param, value):
        if value is None or len(value) == 0:
            raise click.BadParameter('A Crash Id needs to be specified')
        else:
            return value

    return click.option('-c', '--crash',
                        type=click.STRING,
                        help='Specify the Crash Id.',
                        callback=callback)(func)


def page_option(func):
    """Get a decorator for the Page index input"""

    return click.option('-p', '--page',
                        help='optional, used for pagination',
                        default=1)(func)


def page_size_option(func):
    """Get a decorator for the Page index input"""

    return click.option('-ps', '--page-size',
                        help='optional, the number of items to be present in the response(25, 50, 100), default is 25',
                        type=click.Choice([25, 50, 100]),
                        default=25)(func)


def date_option(*param_decls):
    """Get a decorator for a Date Option input"""

    DATE_PATTERN = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')

    def decorator(f):
        def callback(ctx, param, value):
            if value is None or len(value) == 0:
                raise click.BadParameter('A Date needs to be specified')
            elif not DATE_PATTERN.match(value):
                raise click.BadParameter('A Date needs to be specified in YYYY-MM-DD format')
            else:
                return value

        return click.option(*param_decls,
                            type=click.STRING,
                            help='required, set to YYYY-MM-DD',
                            callback=callback)(f)

    return decorator
