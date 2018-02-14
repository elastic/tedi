import os
from pathlib import Path

from ..paths import get_render_path, get_template_path, make_render_path


def test_make_render_path():
    src = Path(get_template_path()) / 'one' / 'two'
    dst = make_render_path(src)
    assert dst == Path(os.path.join(str(get_render_path()), 'one', 'two'))
