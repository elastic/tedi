import click
import pyconfig
from typing import Tuple
from . import commands
from .logging import getLogger
from .process import fail

logger = getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
def render(fact):
    """Render build contexts (.tedi/*)."""
    logger.debug('render subcommand called from cli')
    store_fact_flags(fact)
    commands.clean()
    commands.render()


@cli.command()
@click.option('--clean-assets', is_flag=True, help='Also remove assets.')
def clean(clean_assets: bool):
    """Remove rendered files and downloaded assets."""
    logger.debug('clean subcommand called from cli')
    pyconfig.set('cli.flags.clean-assets', clean_assets)
    commands.clean()


@cli.command()
@click.option('--clean-assets', is_flag=True, help='Reaquire assets.')
@click.option('--asset-set', default='default', help='Specify the asset set to build with.')
@click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
def build(clean_assets: bool, asset_set: str, fact):
    """Build images."""
    logger.debug('build subcommand called from cli')
    pyconfig.set('cli.flags.asset-set', asset_set)
    pyconfig.set('cli.flags.clean-assets', clean_assets)
    store_fact_flags(fact)
    # FIXME: Should we auto-clean assets if the assetset changes?
    commands.clean()
    commands.acquire()
    commands.render()
    commands.build()


@cli.command()
@click.option('--asset-set', default='default', help='Specify the asset set to acquire.')
@click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
def acquire(asset_set: str, fact):
    """Acquire assets."""
    logger.debug('acquire subcommand called from cli')
    pyconfig.set('cli.flags.asset-set', asset_set)
    store_fact_flags(fact)

    # Since the user explicitly called "acquire", make sure they get fresh assets
    # by cleaning the assets dir first.
    pyconfig.set('cli.flags.clean-assets', True)
    commands.clean()

    commands.acquire()


def store_fact_flags(flag_args: Tuple[str]) -> None:
    """Take "--fact" flags from the CLI and store them in the config as a dict."""
    facts = {}

    for arg in flag_args:
        if ':' not in arg:
            logger.critical('Arguments to "--fact" must be colon seperated.')
            logger.critical('Like: "tedi --fact=temperature:hot')
            fail()
        fact, value = arg.split(':', 1)
        logger.debug(f'Setting fact from cli: "{fact}" == "{value}"')
        facts[fact] = value

    pyconfig.set('cli.flags.fact', facts)
