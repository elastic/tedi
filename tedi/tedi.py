import click
import os
import shutil

from .paths import render_path


@click.group()
def cli():
    pass


@cli.command()
def render():
    """Render the templates to static files"""
    print('Consider them rendered.')


@cli.command()
def clean():
    """Remove all rendered files"""
    if render_path.exists():
        shutil.rmtree(str(render_path))
        render_path.mkdir()
