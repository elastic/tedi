from pathlib import Path
from pytest import fixture
from ..fileset import Fileset


@fixture
def fileset() -> Fileset:
    return Fileset(Path('tedi/tests/fixtures/projects/simple'))


def test_top_dir_is_a_path(fileset):
    assert isinstance(fileset.top_dir, Path)


def test_repr_is_valid_python(fileset):
    reparsed = eval(fileset.__repr__())
    assert isinstance(reparsed, Fileset)
    assert fileset.top_dir == reparsed.top_dir


def test_fileset_is_a_set_of_paths(fileset):
    assert len(list(fileset)) > 5
    assert all([isinstance(f, Path) for f in fileset])


def test_fileset_files_are_relative_to_top_dir(fileset):
    for f in fileset:
        assert not f.is_absolute()
        top = fileset.top_dir
        assert (top / f.relative_to(top)).exists()


def test_fileset_contains_subdirectories(fileset):
    for f in fileset.files:
        print(f.parts[-3:])
        if f.parts[-3:] == ('deep', 'directory', 'structure'):
            return
    raise AssertionError
