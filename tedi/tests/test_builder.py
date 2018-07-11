import docker
import shutil
from pathlib import Path
from pytest import fixture
from ..builder import Builder
from ..factset import Factset
from uuid import uuid4


source_dir = Path('tedi/tests/fixtures/projects/simple')
target_dir = Path('target.test.tmp')
assert source_dir.exists()

docker_client = docker.from_env()
test_image_name = f'tedi-test-{uuid4()}'


@fixture
def builder():
    if target_dir.exists():
        shutil.rmtree(str(target_dir))
    facts = Factset(cow_color='brown')
    try:
        docker_client.images.remove(test_image_name)
    except docker.errors.ImageNotFound:
        pass
    return Builder(test_image_name, source_dir, target_dir, facts)


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

    image_found_locally = False
    for image in docker_client.images.list():
        for tag in image.tags:
            print(tag)
        if f'{test_image_name}:latest' in image.tags:
            image_found_locally = True
    assert image_found_locally
