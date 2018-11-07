import logging
import yaml
from . import cli
from .paths import Paths
from .image import Image
from .factset import Factset
from .assetset import Assetset
from .process import fail

logger = logging.getLogger('tedi.project')
paths = Paths()


class Project():
    def __init__(self, path=paths.tedi_path):
        self.path = path
        config_path = self.path / 'tedi.yml'

        try:
            with open(config_path) as config_file:
                self.config = yaml.load(config_file.read())
        except FileNotFoundError:
            logger.critical(f'No configuration file found at {config_path.resolve()}')
            fail()
        if self.config is None:
            logger.critical(f'Config file "{self.path}/tedi.yml" is empty.')
            fail()
        logger.debug(f'Loaded project config from {self.path}: {self.config}')

        if 'facts' in self.config:
            self.facts = Factset(**self.config['facts'])
        else:
            self.facts = Factset()

        # Set any facts that were passed as CLI flags.
        self.facts.update(cli.get_flag('fact', {}))

        # A project has a collection of one or more images.
        self.images = []
        for image_name, image_config in self.config['images'].items():
            self.images.append(Image.from_config(image_name, image_config, self.facts))

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
        """Render the build contexts."""
        for image in self.images:
            image.render()

    def build(self):
        """Build all Images."""
        for image in self.images:
            image.build()

    def acquire_assets(self):
        asset_set = cli.get_flag('asset-set')
        if not self.asset_sets:
            logger.debug('No asset sets for this project. Will not acquire any files.')
            return

        if asset_set not in self.asset_sets:
            logger.critical(f'Asset set "{asset_set}" not defined in tedi.yml.')
            fail()

        self.asset_sets[asset_set].acquire()
