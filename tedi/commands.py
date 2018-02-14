import logging
import os
import shutil
from jinja2 import Template
from pathlib import Path
from .paths import get_render_path, get_template_path, make_render_path
from .facts import Facts

logger = logging.getLogger('tedi')


def render_template_file(src, dst):
    """Render a template from src Path to dst Path with Jinja2."""
    with src.open() as template_file:
        template = Template(template_file.read())
    with dst.open('w') as rendered_file:
        rendered_file.write(template.render(Facts().get_all()))


def render():
    """Render the templates to static files"""
    for root, subdirs, files in os.walk(str(get_template_path())):
        new_dir = make_render_path(Path(root))
        logger.debug("Creating render dir: %s" % new_dir)
        new_dir.mkdir(parents=True)

        for f in files:
            src = Path(root) / f
            dst = make_render_path(src)
            logger.debug("Rendering: %s -> %s" % (src, dst))
            render_template_file(src, dst)
    print('Consider them rendered.')


def clean():
    """Remove all rendered files"""
    if get_render_path().exists():
        logger.debug('Recursively deleting render path: %s' % str(get_render_path()))
        shutil.rmtree(str(get_render_path()))
