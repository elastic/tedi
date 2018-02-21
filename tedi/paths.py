import logging
import pyconfig
from pathlib import Path

logger = logging.getLogger('tedi.paths')


class Paths(object):
    @property
    def template_path(self):
        return Path(pyconfig.get('template_path', 'templates'))

    @property
    def render_path(self):
        return Path(pyconfig.get('render_path', 'renders'))

    def make_render_path(self, path_to_template_file, suffix=None):
        """Given a Path in the template dir, return the matched Path in the render dir

        For example, if template_path is "input/tree/templates", the following
        translations will happen:

        input/tree/templates/README -> renders/README
        input/tree/templates/image/Dockerfile -> renders/image/Dockerfile

        If suffix is specified, it is added like this:

        input/tree/templates/image/... -> input/tree/templates/image-suffix/...
        """
        depth_of_template_root_dir = len(self.template_path.parts)
        trailing_components = list(path_to_template_file.parts[depth_of_template_root_dir:])
        if suffix and trailing_components:
            trailing_components[0] += '-' + suffix
        return self.render_path / Path(*trailing_components)
