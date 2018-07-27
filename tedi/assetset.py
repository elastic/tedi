from typing import List
from .asset import Asset
from .logging import getLogger
from .paths import Paths

logger = getLogger(__name__)
paths = Paths()


class Assetset():
    def __init__(self, assets: List[Asset]) -> None:
        self.assets = assets
        logger.debug(f'New Assetset: {self}')

    def __repr__(self):
        return f'Assetset({self.assets})'

    def acquire(self):
        for asset in self.assets:
            asset.acquire(paths.assets_path)
