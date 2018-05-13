from pytest import fixture
from ..asset import Asset
from ..paths import Paths

paths = Paths()


@fixture
def asset() -> Asset:
    return Asset(
        filename='local-asset-fixture.tar.gz',
        source='file:///etc/issue',
    )


def test_aquire_creates_the_local_file(asset):
    asset.acquire()
    assert (paths.assets_path / 'local-asset-fixture.tar.gz').exists()
