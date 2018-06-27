import click
from . import commands
from .logging import getLogger

logger = getLogger(__name__)


@click.group()
def cli():
    """A empty command group to create subcommands like 'tedi render'"""
    pass


@cli.command()
def render():
    """Render the projects to static files"""
    logger.debug('render subcommand called from cli')
    commands.clean()
    commands.render()


@cli.command()
@click.option('--clean-assets', is_flag=True, help='Also remove assets.')
def clean(clean_assets):
    """Remove all rendered files and (optionally) downloaded assets"""
    logger.debug('clean subcommand called from cli')
    commands.clean(clean_assets)


@cli.command()
@click.option('--clean-assets', is_flag=True, help='Reaquire assets.')
def build(clean_assets):
    """Render the projects to static files"""
    logger.debug('build subcommand called from cli')
    commands.clean(clean_assets)
    commands.render()
    commands.build()
