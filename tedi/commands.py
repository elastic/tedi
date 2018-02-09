import logging
import os
import shutil
from pathlib import Path

from .paths import make_render_path, render_path, template_path

logger = logging.getLogger('tedi')

def render():
    """Render the templates to static files"""
    for root, subdirs, files in os.walk('templates'):
        for subdir in subdirs:
            new_dir = Path(root.replace(str(template_path), str(render_path))) / subdir
            logger.debug("Creating directory: %s" % new_dir)
            new_dir.mkdir()
        for f in files:
            src = Path(root) / f
            dst = make_render_path(src)
            logger.debug("Copying plain file: %s -> %s" % (src, dst))
            shutil.copy(str(src), str(dst))
    print('Consider them rendered.')


def clean():
    """Remove all rendered files"""
    if render_path.exists():
        shutil.rmtree(str(render_path))
        render_path.mkdir()
