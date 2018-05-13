from .asset import Asset
from typing import List


class Assetset():
    def __init__(self, assets: List[Asset]) -> None:
        self.assets = assets
