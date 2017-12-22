import click
import os
import tedi.commands as commands


@click.group()
def cli():
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
