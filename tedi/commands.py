import shutil
from .paths import render_path


def render():
    """Render the templates to static files"""
    print('Consider them rendered.')


def clean():
    """Remove all rendered files"""
    if render_path.exists():
        shutil.rmtree(str(render_path))
        render_path.mkdir()
