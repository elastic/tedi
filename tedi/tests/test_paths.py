from ..paths import Paths

paths = Paths()


def test_make_render_path():
    src = paths.template_path / 'one' / 'two'
    dst = paths.make_render_path(src)
    assert dst == paths.render_path / 'one' / 'two'
