import docker
import glob
import logging
import os
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
            image_flavor='oss'
        ),
    ).render()


def clean():
    """Remove all rendered files"""
    if paths.renders_path.exists():
        logger.debug('Recursively deleting render path: %s' % str(paths.renders_path))
        shutil.rmtree(str(paths.renders_path))


def build():
    """Build the images from the rendered files"""
    client = docker.from_env()
    projects = os.listdir(str(paths.renders_path))
    print(projects)
    for project in projects:
        logger.info('Building %s...' % project)
        image, build_log = client.images.build(
            path=os.path.join(paths.renders_path, project),
            tag=f'{project}:tedi'
        )
        for line in build_log:
            if 'stream' in line:
                logger.debug(line['stream'])
