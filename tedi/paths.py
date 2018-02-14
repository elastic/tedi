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
