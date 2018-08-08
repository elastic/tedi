import click
from . import commands
from .logging import getLogger

logger = getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
def render(fact):
    """Render build contexts (.tedi/*)."""
    logger.debug('render subcommand called from cli')
    commands.clean()
    commands.render(cli_facts=fact)


@cli.command()
@click.option('--clean-assets', is_flag=True, help='Also remove assets.')
def clean(clean_assets: bool):
    """Remove rendered files and downloaded assets."""
    logger.debug('clean subcommand called from cli')
    commands.clean(clean_assets)


@cli.command()
@click.option('--clean-assets', is_flag=True, help='Reaquire assets.')
@click.option('--asset-set', default='default', help='Specify the asset set to build with.')
@click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
def build(clean_assets: bool, asset_set: str, fact):
    """Build images."""
    logger.debug('build subcommand called from cli')
    # FIXME: Should we auto-clean assets if the assetset changes?
    commands.clean(clean_assets)
    commands.acquire(cli_facts=fact, asset_set=asset_set)
    commands.render(cli_facts=fact)
    commands.build(cli_facts=fact)


@cli.command()
@click.option('--asset-set', default='default', help='Specify the asset set to acquire.')
@click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
def acquire(asset_set: str, fact):
    """Acquire assets."""
    logger.debug('acquire subcommand called from cli')
    # Since the user explicitly called "acquire", make sure they get fresh assets
    # by cleaning the assets dir first.
    commands.clean(clean_assets=True)
    commands.acquire(cli_facts=fact, asset_set=asset_set)
