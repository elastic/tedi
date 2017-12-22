import click
import os
import shutil

from .constants import render_dir


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
    if os.path.isdir(render_dir):
        shutil.rmtree(render_dir)
        os.mkdir(render_dir)
