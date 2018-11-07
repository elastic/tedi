from pathlib import Path


class Paths(object):
    @property
    def tedi_path(self):
        return Path('.tedi')

    @property
    def assets_path(self):
        return self.tedi_path / 'assets'

    @property
    def build_path(self):
        return self.tedi_path / 'build'

    @property
    def template_path(self):
        return self.tedi_path / 'template'
