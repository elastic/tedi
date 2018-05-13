from uuid import uuid4
from click.testing import CliRunner
from ..cli import cli
from ..paths import Paths

paths = Paths()


def invoke(command):
    return CliRunner().invoke(cli, command.split())


def output_of(command):
    return invoke(command).output


def assert_in_file(test_file, string):
    invoke('render')
    assert string in (paths.renders_path / test_file).open().read()


def assert_command_cleans_path(path, command):
    """Given a TEDI subcommand name, assert that it cleans up rendered files"""
    path.mkdir(parents=True, exist_ok=True)
    canary = path / ('test-canary-%s' % uuid4())
    canary.touch()
    invoke(command)
    assert canary.exists() is False


def test_render_command_has_valid_help_text():
    assert 'Render' in output_of('render --help')


def test_clean_command_removes_rendered_files():
    assert_command_cleans_path(paths.renders_path, 'clean')


def test_render_command_cleans_renders_path():
    assert_command_cleans_path(paths.renders_path, 'render')


def test_clean_command_removes_assets_with_clean_assets_flag():
    assert_command_cleans_path(paths.assets_path, 'clean --clean-assets')


def test_build_command_removes_assets_with_clean_assets_flag():
    assert_command_cleans_path(paths.assets_path, 'build --clean-assets')
