from typing import List
from .asset import Asset
from .paths import Paths

paths = Paths()


class Assetset():
    def __init__(self, assets: List[Asset]) -> None:
        self.assets = assets

    def acquire(self):
        for asset in self.assets:
            asset.acquire(paths.assets_path)
