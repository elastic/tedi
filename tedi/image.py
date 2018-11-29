import docker
import os
import shutil
from pathlib import Path
from typing import List
from .fileset import Fileset
from .jinja_renderer import JinjaRenderer
from .factset import Factset
from .logging import getLogger
from .paths import Paths

logger = getLogger(__name__)
paths = Paths()


class Image():
    def __init__(self, image_name: str, facts: Factset = Factset(),
                 image_aliases: List[str] = [], path=paths.template_path) -> None:
        self.image_name = image_name
        self.image_aliases = image_aliases
        self.facts = facts
        self.source_dir = path

        self.target_dir = paths.build_path / image_name
        self.files = Fileset(self.source_dir)
        self.renderer = JinjaRenderer(self.facts)
        self.docker = docker.from_env()
        logger.debug(f'New Image: {self}')

    @classmethod
    def from_config(cls, name, config, facts: Factset = Factset()):
        """Create an Image using a configuration block from tedi.yml

        Like this:

          nyancat:
            aliases:
              - rainbow_cat
              - happy_cat
            facts:
              colorful: true

        Facts defined in the configuration will be added to the Factset
        passed in as the "facts" parameter. This is useful for adding
        image-specific facts on top of more general facts from the project.

        The underlying Factset is not mutated. An independant copy is made
        for the Image's use.
        """
        if not config:
            config = {}

        logger.debug(f'Loaded image config for {name}: {config}')
        facts = facts.copy()

        if 'facts' in config:
            facts.update(config['facts'])

        return cls(
            image_name=name,
            facts=facts,
            image_aliases=config.get('aliases', [])
        )

    def __repr__(self):
        return "Image(source_dir='%s', target_dir='%s', facts=%s)" % \
            (self.files.top_dir, self.target_dir, self.renderer.facts)

    def render(self):
        """Render the template files to a ready-to-build directory."""
        if self.target_dir.exists():
            logger.debug(f'Removing old build context: {self.target_dir}')
            shutil.rmtree(str(self.target_dir))

        logger.info(f'Rendering build context: {self.source_dir} -> {self.target_dir}')
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
        self.link_assets()

    def link_assets(self):
        """Make assets available in the build context via hard links."""
        if not paths.assets_path.exists():
            return

        for asset in os.listdir(paths.assets_path):
            source = paths.assets_path / asset
            target = self.target_dir / asset
            logger.debug(f'Hard linking: {source} -> {target}')
            try:
                os.link(source, target)
            except PermissionError:
                # This happens on vboxfs, as often used with Vagrant.
                logger.warn(f'Hard linking failed. Copying: {source} -> {target}')
                shutil.copyfile(source, target)

    def build(self):
        """Run a "docker build" on the rendered image files."""
        dockerfile = self.target_dir / 'Dockerfile'
        if not dockerfile.exists():
            logger.warn(f'No Dockerfile found at {dockerfile}. Cannot build {self.image_name}.')
            return

        tag = self.facts["image_tag"]
        fqin = f'{self.image_name}:{tag}'

        logger.info(f'Building image: {fqin}')

        image, build_log = self.docker.images.build(
            path=str(self.target_dir),
            # Frustratingly, Docker change their minds about which part is the "tag".
            # We say that the part after the colon is the tag, like ":latest".
            # Docker does too, most of the time, but for this function, the "tag"
            # parameter takes a fully qualified image name.
            tag=fqin
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
            logger.info(f'Aliasing image: {self.image_name}:{tag} -> {alias}:{tag}')
            image.tag(f'{alias}:{tag}')
