import logging
import pyconfig
from pathlib import Path

logger = logging.getLogger('tedi.paths')


class Paths(object):
    @property
    def assets_path(self):
        return Path(pyconfig.get('assets_path', 'assets'))

    @property
    def projects_path(self):
        return Path(pyconfig.get('projects_path', 'projects'))

    @property
    def renders_path(self):
        return Path(pyconfig.get('renders_path', 'renders'))
