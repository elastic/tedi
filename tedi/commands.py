import shutil
from .paths import Paths
from .project import Project
from .logging import getLogger

logger = getLogger(__name__)
paths = Paths()

projects = []
for path in paths.projects_path.glob('*'):
    projects.append(Project(path))
    assert projects


def die(message, exit_code=1):
    logger.error(message)
    raise SystemExit(exit_code)


def render():
    """Render the projects to static files"""
    for project in projects:
        project.render()


def clean(clean_assets=False):
    """Remove all rendered files and optionally assets"""
    if paths.renders_path.exists():
        logger.debug('Recursively deleting render path: %s' % str(paths.renders_path))
        shutil.rmtree(str(paths.renders_path))

    if clean_assets and paths.assets_path.exists():
        logger.debug('Recursively deleting assets path: %s' % str(paths.assets_path))
        shutil.rmtree(str(paths.assets_path))


def build():
    """Build the images from the rendered files"""
    for project in projects:
        project.build()
