import os
import sys
import click
import json

from hockeyapp import __version__


CONTEXT_SETTINGS = dict(
    auto_envvar_prefix='HOCKEYAPP',
    help_option_names=["-h", "--help"]
)


class Config(object):

    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()
        self.token = None

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

    def format_json(self, json_response):
        """Logs a request as JSON to stderr"""
        self.log(json.dumps(json_response, indent=2))


pass_context = click.make_pass_decorator(Config, ensure=True)
commands_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))


class HockeyAppCLI(click.MultiCommand):

    def list_commands(self, ctx):
        cmds = []
        for filename in os.listdir(commands_folder):
            if filename.endswith('.py') and not filename.startswith("__init__"):
                cmds.append(filename[:-3])
        cmds.sort()
        print(cmds)
        return cmds

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('hockeyapp.commands.' + name, None, None, ['cli'])
        except ImportError:
            raise click.UsageError('No such command "%s"' % name, ctx)
            return
        return mod.cli


@click.command(cls=HockeyAppCLI, context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode.')
@pass_context
def cli(ctx, verbose):
    """The HockeyApp CLI.

       See 'hockeyapp COMMAND --help' for more information on a specific command."""
    ctx.verbose = verbose
