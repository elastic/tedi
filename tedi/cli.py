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
@click_log.simple_verbosity_option(logger)
def clean():
    """Remove all rendered files"""
    commands.clean()


@cli.command()
@click_log.simple_verbosity_option(logger)
def build():
    """Render the projects to static files"""
    commands.clean()
    commands.render()
    commands.build()
