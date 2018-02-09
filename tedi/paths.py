import os
from pathlib import Path


template_path = Path('templates')
render_path = Path('renders')


def make_render_path(template_path):
    """Given a Path in the template dir, return the matched Path in the render dir"""
    return Path(render_path) / os.path.sep.join(template_path.parts[1:])
