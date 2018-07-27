import shutil
from .paths import Paths
from .project import Project
from .logging import getLogger

logger = getLogger(__name__)
paths = Paths()


def die(message, exit_code=1):
    logger.error(message)
    raise SystemExit(exit_code)


def render():
    """Render the projects to static files"""
    Project().render()


def clean(clean_assets=False):
    """Remove all rendered files and optionally assets"""
    if paths.render_path.exists():
        logger.debug('Recursively deleting render path: %s' % str(paths.render_path))
        shutil.rmtree(str(paths.render_path))

    if clean_assets and paths.assets_path.exists():
        logger.debug('Recursively deleting asset path: %s' % str(paths.assets_path))
        shutil.rmtree(str(paths.assets_path))


def build():
    """Build the images from the rendered files"""
    Project().build()


def acquire(asset_set=None):
    """Acquire assets."""
    Project().acquire_assets(asset_set)
