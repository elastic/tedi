import logging
from pathlib import Path

logger = logging.getLogger('tedi.paths')


class Paths(object):
    @property
    def assets_path(self):
        return Path('assets')

    @property
    def projects_path(self):
        return Path('projects')

    @property
    def renders_path(self):
        return Path('renders')
