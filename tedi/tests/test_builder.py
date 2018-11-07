import docker
import shutil
from pathlib import Path
from pytest import fixture
from ..image import Image
from ..factset import Factset
from uuid import uuid4

test_run_id = uuid4()
source_dir = Path('tedi/tests/fixtures/projects/simple/template')
target_dir = Path(f'.tedi/build/tedi-test-{test_run_id}')
assets_dir = Path(f'.tedi/assets')
assert source_dir.exists()

docker_client = docker.from_env()
test_image_name = f'tedi-test-{test_run_id}'
test_image_aliases = [
    f'tedi-test-alias1-{test_run_id}',
    f'tedi-test-alias2-{test_run_id}',
    f'tedi.example.org/tedi-test-{test_run_id}'
]


@fixture
def image():
    if target_dir.exists():
        shutil.rmtree(str(target_dir))
    facts = Factset(cow_color='brown')
    try:
        docker_client.images.remove(test_image_name)
    except docker.errors.ImageNotFound:
        pass
    return Image(test_image_name, facts, image_aliases=test_image_aliases, path=source_dir)


def image_exists(name, tag='latest'):
    image_found = False
    for image in docker_client.images.list():
        for fqin in image.tags:
            print(fqin)
        if f'{name}:{tag}' in image.tags:
            image_found = True
    return image_found


def test_render_creates_the_target_dir(image):
    image.render()
    assert target_dir.exists()
    assert target_dir.is_dir()


def test_render_copies_normal_files(image):
    image.render()
    assert (target_dir / 'Dockerfile').exists()


def test_render_links_files_from_the_assets_dir(image):
    assets_dir.mkdir(parents=True, exist_ok=True)
    canary_id = str(uuid4())
    asset = (assets_dir / canary_id)
    with asset.open('w') as f:
        f.write('asset_contents')

    image.render()
    assert (target_dir / canary_id).exists()


def test_render_renders_jinja2_templates(image):
    target = (target_dir / 'README.md')
    image.render()
    assert target.exists()
    with target.open() as f:
        assert 'How now, brown cow?' in f.read()


def test_build_creates_a_docker_image(image):
    image.render()
    image.build()
    assert image_exists(test_image_name)


def test_names_image_with_all_aliases(image):
    image.render()
    image.build()
    for alias in test_image_aliases:
        assert image_exists(alias)


def test_from_config_updates_facts_from_the_config():
    config = {
        'facts': {
            'freshness': 'intense'
        }
    }

    image = Image.from_config(
        name=test_image_name,
        config=config,
    )

    assert image.facts['freshness'] == 'intense'


def test_images_have_independant_factsets():
    base_facts = Factset(color='black')

    config_one = {'facts': {'color': 'red'}}
    image_one = Image.from_config(name=test_image_name, config=config_one, facts=base_facts)

    config_two = {'facts': {'color': 'blue'}}
    image_two = Image.from_config(name=test_image_name, config=config_two, facts=base_facts)

    assert base_facts['color'] == 'black'
    assert image_one.facts['color'] == 'red'
    assert image_two.facts['color'] == 'blue'
