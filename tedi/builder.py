import docker
import logging
import shutil
from pathlib import Path
from .fileset import Fileset
from .jinja_renderer import JinjaRenderer


logger = logging.getLogger('tedi.builder')


class Builder():
    def __init__(self, image_name, source_dir, target_dir, facts):
        self.image_name = image_name
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
        logger.info(f'Rendering project: {self.source_dir} -> {self.target_dir}')
        if self.target_dir.exists():
            logger.debug(f'Removing old rendered project: {self.target_dir}')
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
        logger.info('Building %s...' % self.target_dir)
        print(self.target_dir)
        image, build_log = self.docker.images.build(
            path=str(self.target_dir),
            tag=f'{self.image_name}'
        )
        for line in build_log:
            if 'stream' in line:
                logger.debug(line['stream'])