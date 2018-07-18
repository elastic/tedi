import click
from . import commands
from .logging import getLogger

logger = getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
def render():
    """Render build contexts (.tedi/*)."""
    logger.debug('render subcommand called from cli')
    commands.clean()
    commands.render()


@cli.command()
@click.option('--clean-assets', is_flag=True, help='Also remove assets.')
def clean(clean_assets):
    """Remove rendered files and downloaded assets."""
    logger.debug('clean subcommand called from cli')
    commands.clean(clean_assets)


@cli.command()
@click.option('--clean-assets', is_flag=True, help='Reaquire assets.')
def build(clean_assets):
    """Build images."""
    logger.debug('build subcommand called from cli')
    commands.clean(clean_assets)
    commands.render()
    commands.build()
