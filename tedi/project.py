import yaml
import logging
from .paths import Paths
from .builder import Builder
from .factset import Factset
from .assetset import Assetset
from .process import fail

logger = logging.getLogger('tedi.project')
paths = Paths()


class Project():
    def __init__(self, path=paths.project_path, cli_facts=()):
        self.path = path
        config_path = path / 'tedi.yml'

        try:
            with open(config_path) as config_file:
                self.config = yaml.load(config_file.read())
        except FileNotFoundError:
            logger.critical(f'No configuration file found at {config_path.resolve()}')
            fail()

        assert self.config  # Because the YAML library returns None for empty files.
        logger.debug(f'Loaded project config from {self.path}: {self.config}')

        if 'facts' in self.config:
            self.facts = Factset(**self.config['facts'])
        else:
            self.facts = Factset()

        if cli_facts:
            for fact_string in cli_facts:
                fact, value = fact_string.split(':', 1)
                self.facts[fact] = value

        # A project has a collection of one or more image builders.
        self.builders = []
        for image_name, image_config in self.config['images'].items():
            self.builders.append(Builder.from_config(image_name, image_config, self.facts))

        # A project can have "asset sets" ie. files to be downloaded or copied
        # into the build context.
        self.asset_sets = {}
        if 'asset_sets' in self.config:
            for name, assets in self.config['asset_sets'].items():
                if assets:
                    self.asset_sets[name] = Assetset.from_config(assets, self.facts)
                else:
                    # Die with a helpful message if an empty asset set was declared.
                    logger.critical(f'Empty asset set "{name}" in tedi.yml')
                    fail()

    def __repr__(self):
        return f'Project("{self.path}")'

    def render(self):
        for builder in self.builders:
            builder.render()

    def build(self):
        """Build all Builders.

        Optionally specify an explicit tag like "7.0.0" or "latest".
        """
        for builder in self.builders:
            builder.build()

    def acquire_assets(self, asset_set_name: str):
        if not self.asset_sets:
            logger.debug('No asset sets for this project. Will not acquire any files.')
            return

        if asset_set_name not in self.asset_sets:
            logger.critical(f'Asset set "{asset_set_name}" not defined in tedi.yml.')
            fail()

        self.asset_sets[asset_set_name].acquire()
