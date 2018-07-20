import docker
import shutil
from pathlib import Path
from typing import List
from .fileset import Fileset
from .jinja_renderer import JinjaRenderer
from .factset import Factset
from .logging import getLogger

logger = getLogger(__name__)


class Builder():
    def __init__(self, image_name: str, source_dir: Path, target_dir: Path,
                 facts: Factset, image_aliases: List[str]=None) -> None:
        self.image_name = f'{image_name}:{facts["image_tag"]}'
        if image_aliases:
            self.image_aliases = [f'{alias}:{facts["image_tag"]}' for alias in image_aliases]
        else:
            self.image_aliases = []

        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.files = Fileset(self.source_dir)
        self.renderer = JinjaRenderer(facts)
        self.docker = docker.from_env()
        logger.debug(f'New Builder: {self}')

    def __repr__(self):
        return "Builder(source_dir='%s', target_dir='%s', facts=%s)" % \
            (self.files.top_dir, self.target_dir, self.renderer.facts)

    def render(self):
        """Render the template files to a ready-to-build directory."""
        logger.info(f'Rendering {self.image_name}: {self.source_dir} -> {self.target_dir}')
        if self.target_dir.exists():
            logger.debug(f'Removing old render: {self.target_dir}')
            shutil.rmtree(str(self.target_dir))
        self.target_dir.mkdir(parents=True)

        for source in self.files:
            target = self.target_dir / source.relative_to(self.files.top_dir)
            if source.is_dir():
                logger.debug(f'Creating directory: {target}')
                target.mkdir()
            elif source.suffix == '.j2':
                target = Path(target.with_suffix(''))  # Remove '.j2'
                logger.debug(f'Rendering file: {source} -> {target}')
                with target.open('w') as f:
                    f.write(self.renderer.render(source))
            else:
                logger.debug(f'Copying file: {source} -> {target}')
                shutil.copy2(str(source), str(target))

    def build(self):
        """Run a "docker build" on the rendered image files."""
        dockerfile = self.target_dir / 'Dockerfile'
        if not dockerfile.exists():
            logger.warn(f'No Dockerfile found at {dockerfile}. Cannot build {self.image_name}.')
            return

        logger.info(f'Building {self.image_name}...')
        image, build_log = self.docker.images.build(
            path=str(self.target_dir),
            tag=f'{self.image_name}'
        )

        # The output you'd normally get on the terminal from `docker build` can
        # be found in the build log, along with some extra metadata lines we
        # don't care about. The good stuff is in the lines that have a 'stream'
        # field.
        for line in build_log:
            if 'stream' in line:
                message = line['stream'].strip()
                if message:
                    logger.debug(message)

        for alias in self.image_aliases:
            logger.info(f'Tagging {self.image_name} as {alias}')
            image.tag(alias)
