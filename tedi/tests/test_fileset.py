from pathlib import Path
from pytest import fixture
from ..fileset import Fileset


@fixture
def fileset() -> Fileset:
    return Fileset(Path('tedi/tests/fixtures/fileset/simple'))


def test_top_dir_is_a_path(fileset):
    assert isinstance(fileset.top_dir, Path)


def test_fileset_is_a_set_of_paths(fileset):
    assert len(list(fileset)) > 5
    assert all([isinstance(f, Path) for f in fileset])


def test_fileset_files_are_relative_to_top_dir(fileset):
    for f in fileset:
        assert not f.is_absolute()
        top = fileset.top_dir
        assert (top / f.relative_to(top)).exists()


def test_relative_yields_files_relative_to_top_dir(fileset):
    assert Path('Dockerfile') in fileset.relative()
    assert Path('files/file01') in fileset.relative()
    assert Path('deep/directory/structure/deepfile01') in fileset.relative()


def test_fileset_contains_subdirectories(fileset):
    assert Path('deep/directory/structure') in fileset.relative()
