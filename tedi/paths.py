import logging
import os
import pyconfig
from pathlib import Path

logger = logging.getLogger('tedi')


def get_template_path():
    return Path(pyconfig.get('template_path', 'templates'))


def get_render_path():
    return Path(pyconfig.get('render_path', 'renders'))


def make_render_path(template_path):
    """Given a Path in the template dir, return the matched Path in the render dir"""
    return get_render_path() / os.path.sep.join(template_path.parts[1:])


def mkdir_for_render(path):
    """Given a Path in the template dir, create the matching render dir on disk"""
    new_dir = make_render_path(path)
    logger.debug("Creating render dir: %s" % new_dir)
    new_dir.mkdir(parents=True)
