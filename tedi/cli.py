import click
import click_log
import logging
from . import commands

logger = logging.getLogger('tedi')
click_log.basic_config(logger)


@click.group()
def cli():
    """A empty command group to create subcommands like 'tedi render'"""
    pass


@cli.command()
@click_log.simple_verbosity_option(logger)
def render():
    """Render the projects to static files"""
    commands.clean()
    commands.render()


@cli.command()
@click.option('--clean-assets', is_flag=True, help='Also remove assets.')
@click_log.simple_verbosity_option(logger)
def clean(clean_assets):
    """Remove all rendered files and (optionally) downloaded assets"""
    commands.clean(clean_assets)


@cli.command()
@click.option('--clean-assets', is_flag=True, help='Reaquire assets.')
@click_log.simple_verbosity_option(logger)
def build(clean_assets):
    """Render the projects to static files"""
    commands.clean(clean_assets)
    commands.render()
    commands.build()
