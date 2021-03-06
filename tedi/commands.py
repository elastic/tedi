import shutil
from . import cli
from .paths import Paths
from .project import Project
from .logging import getLogger

logger = getLogger(__name__)
paths = Paths()


def render() -> None:
    """Render the projects to static files."""
    Project().render()


def clean() -> None:
    """Remove all rendered files and, optionally, assets."""
    if paths.build_path.exists():
        logger.debug('Recursively deleting render path: %s' % str(paths.build_path))
        shutil.rmtree(str(paths.build_path))

    if cli.get_flag('clean-assets') and paths.assets_path.exists():
        logger.debug('Recursively deleting asset path: %s' % str(paths.assets_path))
        shutil.rmtree(str(paths.assets_path))


def build() -> None:
    """Build the images from the rendered files."""
    Project().build()


def acquire() -> None:
    """Acquire assets."""
    Project().acquire_assets()
