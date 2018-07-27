import yaml
import logging
from .paths import Paths
from .builder import Builder
from .factset import Factset
from .assetset import Assetset
from .asset import Asset
from .process import fail
from .jinja_renderer import JinjaRenderer

logger = logging.getLogger('tedi.project')
paths = Paths()


class Project():
    def __init__(self, path):
        self.path = path
        config_path = self.path / 'tedi.yml'

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

        renderer = JinjaRenderer(self.facts)

        # A project has a collection of one or more image builders.
        self.builders = []
        for image_name, image_config in self.config['images'].items():
            if image_config is None:
                image_config = {}
            logger.debug(f'Loaded builder config for {image_name}: {image_config}')

            # Each image gets it own Factset that inherits from the project Factset.
            image_facts = Factset(**self.facts.to_dict())
            if 'facts' in image_config:
                image_facts.update(image_config['facts'])

            builder = Builder(
                image_name=image_name,
                source_dir=self.path,
                target_dir=paths.render_path / image_name,
                facts=image_facts,
                image_aliases=image_config.get('aliases')
            )
            self.builders.append(builder)

        self.asset_sets = {}
        # FIXME: Teach Assetset to instantiate itself from a config dict.
        # FIXME: ie. Move this logic to the Assetset class.
        if 'asset_sets' in self.config:
            for asset_set_name, asset_configs in self.config['asset_sets'].items():
                assets = []
                for config in asset_configs:
                    if 'filename' not in config or 'source' not in config:
                        logger.critical('Each asset in tedi.yml must declare "filename" and "source".')
                        fail()

                    # Expand any facts in the asset declaration.
                    filename = renderer.render_string(config['filename'])
                    source = renderer.render_string(config['source'])
                    assets.append(Asset(filename, source))
                self.asset_sets[asset_set_name] = Assetset(assets)

    def __repr__(self):
        return f'Project("{self.path}")'

    def render(self):
        for builder in self.builders:
            builder.render()

    def build(self):
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
