import click
import pyconfig
from typing import Any, Tuple
from . import commands
from .logging import getLogger
from .process import fail

logger = getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
def render(fact: Tuple[str]):
    """Render build contexts (.tedi/*)."""
    logger.debug('render subcommand called from cli')
    set_fact_flags(fact)
    commands.clean()
    commands.render()


@cli.command()
@click.option('--clean-assets', is_flag=True, help='Also remove assets.')
def clean(clean_assets: bool):
    """Remove rendered files and downloaded assets."""
    logger.debug('clean subcommand called from cli')
    set_flag('clean-assets', clean_assets)
    commands.clean()


@cli.command()
@click.option('--clean-assets', is_flag=True, help='Reaquire assets.')
@click.option('--asset-set', default='default', help='Specify the asset set to build with.')
@click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
def build(clean_assets: bool, asset_set: str, fact: Tuple[str]):
    """Build images."""
    logger.debug('build subcommand called from cli')
    set_flag('asset-set', asset_set)
    set_flag('clean-assets', clean_assets)
    set_fact_flags(fact)
    # FIXME: Should we auto-clean assets if the assetset changes?
    commands.clean()
    commands.acquire()
    commands.render()
    commands.build()


@cli.command()
@click.option('--asset-set', default='default', help='Specify the asset set to acquire.')
@click.option('--fact', multiple=True, help='Set a fact, like --fact=color:blue.')
def acquire(asset_set: str, fact: Tuple[str]):
    """Acquire assets."""
    logger.debug('acquire subcommand called from cli')
    set_flag('asset-set', asset_set)
    set_fact_flags(fact)

    # Since the user explicitly called "acquire", make sure they get fresh assets
    # by cleaning the assets dir first.
    set_flag('clean-assets', True)
    commands.clean()

    commands.acquire()


def set_flag(flag: str, value: Any) -> None:
    """Store a CLI flag in the config as "cli.flags.FLAG"."""
    pyconfig.set(f'cli.flags.{flag}', value)


def get_flag(flag: str, default: Any=None) -> Any:
    """Get a CLI flag from the config."""
    return pyconfig.get(f'cli.flags.{flag}', default)


def set_fact_flags(flag_args: Tuple[str]) -> None:
    """Take "--fact" flags from the CLI and store them in the config as a dict."""
    facts = {}

    for arg in flag_args:
        if ':' not in arg:
            logger.critical('Arguments to "--fact" must be colon seperated.')
            logger.critical('Like: "tedi --fact=temperature:hot')
            fail()
        fact, value = arg.split(':', 1)
        logger.debug(f'Setting fact from cli: "{fact}" -> "{value}"')
        facts[fact] = value

    set_flag('fact', facts)
