import os
from pathlib import Path


class Fileset:
    """A Fileset is a collection of all the files under a given top_dir directory."""
    def __init__(self, top_dir):
        self.top_dir = Path(top_dir)
        assert self.top_dir.exists() and self.top_dir.is_dir()

        self.files = []
        for root, subdirs, files in os.walk(str(self.top_dir)):
            for subdir in subdirs:
                files.append(Path(subdir))
            for f in files:
                self.files.append(Path(root) / f)

    def __repr__(self):
        return "Fileset('%s')" % self.top_dir

    def __iter__(self):
        """Iterate over all files in the fileset, relative to top_dir"""
        for f in self.files:
            yield f

    def __len__(self):
        return len(self.files)

    def __contains__(self, path):
        return Path(path) in self.files
