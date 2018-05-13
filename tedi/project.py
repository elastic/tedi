import yaml
import logging
from .paths import Paths
from .builder import Builder
from .factset import Factset

logger = logging.getLogger('tedi.project')
paths = Paths()


class Project():
    def __init__(self, path):
        self.path = path

        self.config = yaml.load(open(self.path / 'tedi.yml').read())
        assert self.config  # Because the YAML library returns None for empty files.
        logger.debug(f'Loaded project config from {self.path}: {self.config}')

        # A project is a collection of one or more image builders.
        self.builders = []
        for image_name, image_config in self.config['images'].items():
            logger.debug(f'Loaded builder config for {image_name}: {image_config}')
            self.builders.append(
                Builder(
                    image_name=image_name,
                    source_dir=self.path,
                    target_dir=paths.renders_path / image_name,
                    facts=Factset(**image_config['facts']),
                )
            )

    def __repr__(self):
        return f'Project("{self.path}")'

    def render(self):
        for builder in self.builders:
            builder.render()

    def build(self):
        for builder in self.builders:
            builder.build()
