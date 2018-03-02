# import docker
import logging
# import os
import shutil
from .paths import Paths
from .builder import Builder
from .factset import Factset


logger = logging.getLogger('tedi.commands')
paths = Paths()


def die(message, exit_code=1):
    logger.error(message)
    raise SystemExit(exit_code)


def render():
    """Render the projects to static files"""
    Builder(
        source_dir='projects/elasticsearch',
        target_dir='renders/elasticsearch',
        facts=Factset(
            artifacts_dir='bob',
            image_flavor='oss',
        ),
    ).render()


def clean():
    """Remove all rendered files"""
    if paths.renders_path.exists():
        logger.debug('Recursively deleting render path: %s' % str(paths.renders_path))
        shutil.rmtree(str(paths.renders_path))


def build():
    """Build the images from the rendered files"""
    pass
    # client = docker.from_env()
    # projects = glob(str(paths.render_path / '*'))
    # for project in projects:
    #     image = os.path.basename(project)
    #     logger.info('Building %s...' % image)
    #     client.images.build(
    #         path=str(project),
    #         tag=os.path.basename(image)
    #     )
