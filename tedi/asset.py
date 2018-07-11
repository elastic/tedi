import wget
from pathlib import Path
from typing import Union
from .logging import getLogger

logger = getLogger(__name__)


class Asset():
    def __init__(self, filename: str, source: str) -> None:
        self.filename = filename
        self.source = source
        logger.debug(f'New Asset: {self}')

    def __repr__(self):
        return f'Asset(filename="{self.filename}", source="{self.source}")'

    def acquire(self, target_dir: Union[Path, str]) -> None:
        target_dir = Path(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f'Aquiring asset to {{ target_dir }}: {self}')
        wget.download(
            self.source,
            str(target_dir / Path(self.filename))
        )
