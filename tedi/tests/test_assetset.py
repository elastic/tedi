from pytest import fixture
from ..assetset import Assetset


@fixture
def assetset() -> Assetset:
    return Assetset([])
