from uuid import uuid4
import shutil
from click.testing import CliRunner
from contextlib import contextmanager
from ..cli import cli
from ..paths import Paths
from .paths import fixtures_path

paths = Paths()


@contextmanager
def project_runner(fixture='simple'):
    fixture_path = (fixtures_path / 'projects' / fixture)
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Copy the project fixture into the isolated filesystem dir.
        shutil.copytree(fixture_path, 'tedi')

        # Monkeypatch a helper method onto the runner to make running commands
        # easier.
        runner.run = lambda command: runner.invoke(cli, command.split())

        # And another for checkout the text output by the command.
        runner.output_of = lambda command: runner.run(command).output
        yield runner


def assert_in_file(runner: CliRunner, test_file, string):
    runner.run('render')
    assert string in (paths.render_path / test_file).open().read()


def assert_command_cleans_path(runner, path, command):
    """Given a TEDI subcommand name, assert that it cleans up rendered files."""
    path.mkdir(parents=True, exist_ok=True)
    canary = path / ('test-canary-%s' % uuid4())
    canary.touch()
    assert runner.run(command).exit_code == 0
    assert canary.exists() is False


def assert_command_acquires_asset(runner, command, filename):
    """Check that an asset file was acquired to the assets dir."""
    assert runner.run('acquire').exit_code == 0
    assert (paths.assets_path / filename).exists()


def test_render_command_has_valid_help_text():
    with project_runner() as runner:
        assert 'Render' in runner.output_of('render --help')


def test_clean_command_removes_rendered_files():
    with project_runner() as runner:
        assert_command_cleans_path(runner, paths.render_path, 'clean')


def test_render_command_cleans_render_path():
    with project_runner() as runner:
        assert_command_cleans_path(runner, paths.render_path, 'render')


def test_clean_command_removes_assets_with_clean_assets_flag():
    with project_runner() as runner:
        assert_command_cleans_path(runner, paths.assets_path, 'clean --clean-assets')


def test_build_command_removes_assets_with_clean_assets_flag():
    with project_runner() as runner:
        assert_command_cleans_path(runner, paths.assets_path, 'build --clean-assets')


def test_acquire_command_acquires_default_assets():
    with project_runner() as runner:
        assert_command_acquires_asset(runner, 'acquire', 'simple-software-1.tar.gz')
