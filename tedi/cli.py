import click
import click_log
import logging
import os
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
    """Render the templates to static files"""
    commands.clean()
    commands.render()


@cli.command()
def clean():
    """Remove all rendered files"""
    commands.clean()
