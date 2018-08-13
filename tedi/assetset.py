from typing import List
from .asset import Asset
from .jinja_renderer import JinjaRenderer
from .logging import getLogger
from .paths import Paths
from .process import fail
from .factset import Factset

logger = getLogger(__name__)
paths = Paths()


class Assetset():
    """A collection of Assets (external files) for use in a build."""
    def __init__(self, assets: List[Asset]) -> None:
        self.assets = assets
        logger.debug(f'New Assetset: {self}')

    @classmethod
    def from_config(cls, config: List[dict]=[], facts: Factset=Factset()):
        """Create an Assetset using a configuration block in tedi.yml

        The YAML form looks like this:

            - filename: bigball.tar.gz
              source: http://example.org/downloads/bigball-v1.tar.gz
            - filename: mince_pie
              source: file:///usr/local/pies/{{ pie_type_fact }}

        This method accepts the above data structure as a Python list. It also
        arranges for template tokens in the configuration to be expanded, using
        the facts available in the Factset.
        """
        assets = []
        renderer = JinjaRenderer(facts)
        for asset in config:
            if 'filename' not in asset or 'source' not in asset:
                logger.critical('Each asset must declare "filename" and "source".')
                fail()

            # Expand any facts in the asset declaration.
            filename = renderer.render_string(asset['filename'])
            source = renderer.render_string(asset['source'])
            assets.append(Asset(filename, source))
        return cls(assets)

    def __repr__(self) -> str:
        return f'Assetset({self.assets})'

    def acquire(self) -> None:
        """Acquire (download) all the assets in this Assetset."""
        for asset in self.assets:
            asset.acquire(paths.assets_path)
