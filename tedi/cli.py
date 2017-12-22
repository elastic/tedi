import click
import os
from . import commands


@click.group()
def cli():
    """A empty command group to create subcommands like 'tedi render'"""
    pass


@cli.command()
def render():
    """Render the templates to static files"""
    commands.clean()
    commands.render()


@cli.command()
def clean():
    """Remove all rendered files"""
    commands.clean()
