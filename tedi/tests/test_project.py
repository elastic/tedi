from pathlib import Path
from pytest import fixture
from ..project import Project
from unittest.mock import Mock


@fixture
def project() -> Project:
    return Project(Path('tedi/tests/fixtures/projects/simple'))


def test_path_is_a_path(project):
    assert isinstance(project.path, Path)


def test_render_calls_render_on_each_builder(project):
    for builder in project.builders:
        builder.render = Mock()
    project.render()
    for builder in project.builders:
        assert builder.render.called


def test_build_calls_build_on_each_builder(project):
    for builder in project.builders:
        builder.build = Mock()
    project.build()
    for builder in project.builders:
        assert builder.build.called
