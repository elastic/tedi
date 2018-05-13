import wget
from pathlib import Path
from typing import Union
from .paths import Paths

assets_path = Paths().assets_path


class Asset():
    def __init__(self, filename: Union[Path, str], source: str) -> None:
        self.filename = filename
        self.local_path = assets_path / Path(filename)
        self.source = source

    def __repr__(self):
        return f'Asset(filename="{self.filename}", source="{self.source}")'

    def acquire(self):
        assets_path.mkdir()
        wget.download(self.source, str(self.local_path))
