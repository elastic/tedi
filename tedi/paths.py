import logging
from pathlib import Path

logger = logging.getLogger('tedi.paths')


class Paths(object):
    @property
    def projects_path(self):
        return Path('projects')

    @property
    def assets_path(self):
        return Path('.tedi/assets')

    @property
    def renders_path(self):
        return Path('renders')
