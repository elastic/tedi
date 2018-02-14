import click
import click_log
import logging
import pyconfig
from . import commands

logger = logging.getLogger('tedi')
click_log.basic_config(logger)


@click.group()
def cli():
    """A empty command group to create subcommands like 'tedi render'"""
    pass


@cli.command()
@click_log.simple_verbosity_option()
@click.option('--render-path', help='Render/copy files to here.')
@click.option('--template-path', help='Source template files from here.')
def render(render_path, template_path):
    """Render the templates to static files"""
    if template_path:
        pyconfig.set('template_path', template_path)
    if render_path:
        pyconfig.set('render_path', render_path)
    commands.clean()
    commands.render()


@cli.command()
@click.option('--render-path', help='Clean rendered files from here.')
def clean(render_path):
    """Remove all rendered files"""
    if render_path:
        pyconfig.set('render_path', render_path)
    commands.clean()
