import logging
import shutil
import yaml
from .paths import Paths
from .builder import Builder
from .factset import Factset


logger = logging.getLogger('tedi.commands')
paths = Paths()

# Scan the project directories and create builders for them.
builders = []
for project_path in paths.projects_path.glob('*'):
    project_config = yaml.load(open(project_path / 'tedi.yml').read())
    assert project_config  # Because the YAML library returns None for empty files.
    logger.debug(f'Loaded project config from {project_path}: {project_config}')
    # A project may have multiple images defined.
    for image_name, image_config in project_config['images'].items():
        logger.debug(f'Loaded image config for {image_name}: {image_config}')
        builders.append(
            Builder(
                image_name=image_name,
                source_dir=project_path,
                target_dir=paths.renders_path / image_name,
                facts=Factset(**image_config['facts']),
            )
        )
    assert builders


def die(message, exit_code=1):
    logger.error(message)
    raise SystemExit(exit_code)


def render():
    """Render the projects to static files"""
    for builder in builders:
        builder.render()


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
    for builder in builders:
        builder.build()
