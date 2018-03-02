import shutil
from pathlib import Path
from pytest import fixture
from ..builder import Builder
from ..factset import Factset


source_dir = Path('tedi/tests/fixtures/fileset/simple')
target_dir = Path('target.test.tmp')
assert source_dir.exists()


@fixture
def builder():
    if target_dir.exists():
        shutil.rmtree(str(target_dir))
    facts = Factset(cow_color='brown')
    return Builder(source_dir, target_dir, facts)


def test_render_creates_the_target_dir(builder):
    builder.render()
    assert target_dir.exists()
    assert target_dir.is_dir()


def test_render_copies_normal_files(builder):
    builder.render()
    assert (target_dir / 'Dockerfile').exists()


def test_render_renders_jinja2_templates(builder):
    target = (target_dir / 'README.md')
    builder.render()
    assert target.exists()
    with target.open() as f:
        assert 'How now, brown cow?' in f.read()
