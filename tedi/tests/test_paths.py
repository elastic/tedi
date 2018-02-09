import os
from pathlib import Path

from ..paths import render_path, template_path, make_render_path


def test_make_render_path():
    src = Path(template_path) / 'one' / 'two'
    dst = make_render_path(src)
    assert dst == Path(os.path.join(str(render_path), 'one', 'two'))
