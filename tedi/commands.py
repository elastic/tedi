import logging
import shutil
from .paths import Paths
from .builder import Builder
from .factset import Factset


logger = logging.getLogger('tedi.commands')
paths = Paths()

builders = [
    Builder(
        image_name='elasticsearch-full',
        source_dir='projects/elasticsearch',
        target_dir='renders/elasticsearch',
        facts=Factset(
            image_flavor='oss'
        ),
    )
]


def die(message, exit_code=1):
    logger.error(message)
    raise SystemExit(exit_code)


def render():
    """Render the projects to static files"""
    for builder in builders:
        builder.render()


def clean():
    """Remove all rendered files"""
    if paths.renders_path.exists():
        logger.debug('Recursively deleting render path: %s' % str(paths.renders_path))
        shutil.rmtree(str(paths.renders_path))


def build():
    """Build the images from the rendered files"""
    for builder in builders:
        builder.build()
