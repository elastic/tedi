from pathlib import Path


class Paths(object):
    @property
    def project_path(self):
        return Path('./tedi')

    @property
    def assets_path(self):
        return Path('.tedi/assets')

    @property
    def build_path(self):
        return Path('.tedi/build')
