import docker
import shutil
from pathlib import Path
from pytest import fixture
from ..builder import Builder
from ..factset import Factset
from uuid import uuid4

test_run_id = uuid4()
source_dir = Path('tedi/tests/fixtures/projects/simple')
target_dir = Path('target.test.tmp')
assert source_dir.exists()

docker_client = docker.from_env()
test_image_name = f'tedi-test-{test_run_id}'
test_image_aliases = [
    f'tedi-test-alias1-{test_run_id}',
    f'tedi-test-alias2-{test_run_id}',
    f'tedi.example.org/tedi-test-{test_run_id}'
]


@fixture
def builder():
    if target_dir.exists():
        shutil.rmtree(str(target_dir))
    facts = Factset(cow_color='brown')
    try:
        docker_client.images.remove(test_image_name)
    except docker.errors.ImageNotFound:
        pass
    return Builder(test_image_name, source_dir, target_dir, facts, image_aliases=test_image_aliases)


def image_exists(name):
    image_found = False
    for image in docker_client.images.list():
        for tag in image.tags:
            print(tag)
        if f'{name}:latest' in image.tags:
            image_found = True
    return image_found


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


def test_build_creates_a_docker_image(builder):
    builder.render()
    builder.build()
    assert image_exists(test_image_name)


def test_tags_image_with_all_aliases(builder):
    builder.render()
    builder.build()
    for alias in test_image_aliases:
        assert image_exists(alias)
