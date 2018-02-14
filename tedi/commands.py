import logging
import os
import shutil
from pathlib import Path
from .paths import get_render_path, get_template_path
from .paths import make_render_path, mkdir_for_render

logger = logging.getLogger('tedi')

def render():
    """Render the templates to static files"""
    for root, subdirs, files in os.walk(str(get_template_path())):
        mkdir_for_render(Path(root))

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
