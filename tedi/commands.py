import logging
import os
import shutil
from pathlib import Path
from .paths import get_render_path, get_template_path, make_render_path

logger = logging.getLogger('tedi')

def render():
    """Render the templates to static files"""
    for root, subdirs, files in os.walk(str(get_template_path())):
        new_dir = make_render_path(Path(root))
        logger.debug("Creating render dir: %s" % new_dir)
        new_dir.mkdir(parents=True)

        for subdir in subdirs:
            new_dir = make_render_path(Path(root) / Path(subdir))
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
    if get_render_path().exists():
        logger.debug('Recursively deleting render path: %s' % str(get_render_path()))
        shutil.rmtree(str(get_render_path()))
