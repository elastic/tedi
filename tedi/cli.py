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
@click.option('--asset-set', default='default', help='Specify the asset set to build with.')
def build(clean_assets, asset_set):
    """Build images."""
    logger.debug('build subcommand called from cli')
    # FIXME: Should we auto-clean assets if the assetset changes?
    commands.clean(clean_assets)
    commands.render()
    commands.acquire(asset_set)
    commands.build()


@cli.command()
@click.option('--asset-set', default='default', help='Specify the asset set to acquire.')
def acquire(asset_set):
    """Acquire assets."""
    logger.debug('acquire subcommand called from cli')
    commands.acquire(asset_set)
