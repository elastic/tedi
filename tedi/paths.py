import logging
import os
import pyconfig
from pathlib import Path

logger = logging.getLogger('tedi')


def get_template_path():
    return Path(pyconfig.get('template_path', 'templates'))


def get_render_path():
    return Path(pyconfig.get('render_path', 'renders'))


def make_render_path(path_to_template_file):
    """Given a Path in the template dir, return the matched Path in the render dir

    For example, if template_path is "input/tree/templates", the following
    translations will happen:

      input/tree/templates/README -> renders/README
      input/tree/templates/image/Dockerfile -> renders/image/Dockerfile
    """
    depth_of_template_root_dir = len(get_template_path().parts)
    trailing_components = path_to_template_file.parts[depth_of_template_root_dir:]
    return get_render_path() / os.path.sep.join(trailing_components)
