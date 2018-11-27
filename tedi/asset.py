import wget
from pathlib import Path
from typing import Union
from urllib.error import HTTPError, URLError
from .logging import getLogger
from .process import fail

logger = getLogger(__name__)


class Asset():
    """A file that can be acquired (downloaded or copied) for use in a build."""
    def __init__(self, filename: str, source: str) -> None:
        self.filename = filename
        self.source = source
        logger.debug(f'New Asset: {self}')

    def __repr__(self):
        return f'Asset(filename="{self.filename}", source="{self.source}")'

    def acquire(self, target_dir: Union[Path, str]) -> None:
        """Acquire this asset from its source.

        The file will be downloaded (or copied) to the target_dir, with the name
        stored in the filename property.
        """
        target_dir = Path(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / self.filename
        if target.exists():
            logger.debug(f'Using cached asset: {self.source} -> {target}')
        else:
            logger.info(f'Acquiring asset: {self.source} -> {target}')
            try:
                wget.download(self.source, str(target), bar=None)
            except (HTTPError, URLError) as e:
                logger.critical(f'Download error: {self.source}')
                logger.critical(e)
                fail()
