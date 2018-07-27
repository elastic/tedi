import wget
import sys
from pathlib import Path
from typing import Union
from urllib.error import HTTPError
from .logging import getLogger
from .process import fail

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
        target = target_dir / self.filename
        if target.exists():
            logger.debug(f'Using cached asset "{target}" for asset {self.source}. ')
        else:
            logger.info(f'Acquiring "{self.source}" to "{target}"')
            try:
                wget.download(self.source, str(target))
                sys.stdout.write('\n')
            except HTTPError as e:
                logger.critical(f'Error downloading {self.source}')
                logger.critical(e)
                fail()
