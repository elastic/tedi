from os.path import dirname, join
from pytest import fixture
from shutil import rmtree
from ..asset import Asset
from ..assetset import Assetset
from ..paths import Paths

paths = Paths()


fixtures_dir_path = join(dirname(__file__), 'fixtures', 'assets')


@fixture
def assetset() -> Assetset:
    asset = Asset(
        filename='acquired_asset',
        source=f'file://{fixtures_dir_path}/text-asset'
    )

    rmtree(str(paths.assets_path))
    return Assetset([asset])


def test_acquire_downloads_files(assetset):
    assetset.acquire()
    assert (paths.assets_path / 'acquired_asset').exists()
