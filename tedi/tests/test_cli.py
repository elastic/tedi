from uuid import uuid4
import shutil
from click.testing import CliRunner
from contextlib import contextmanager
import pyconfig
from ..cli import cli, store_fact_flags
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


def in_file(string, test_file='simple-vanilla/README.md') -> bool:
    return (string in (paths.render_path / test_file).open().read())


def assert_command_cleans_path(runner, path, command):
    """Given a TEDI subcommand name, assert that it cleans up rendered files."""
    path.mkdir(parents=True, exist_ok=True)
    canary = path / ('test-canary-%s' % uuid4())
    canary.touch()
    assert runner.run(command).exit_code == 0
    assert canary.exists() is False


def command_acquires_asset(runner, command, filename):
    """Check that an asset file was acquired to the assets dir."""
    assert runner.run(command).exit_code == 0
    return (paths.assets_path / filename).exists()


def test_render_command_has_valid_help_text():
    with project_runner() as runner:
        assert 'Render' in runner.output_of('render --help')


def test_clean_command_removes_rendered_files():
    with project_runner() as runner:
        assert_command_cleans_path(runner, paths.render_path, 'clean')


def test_render_command_cleans_render_path():
    with project_runner() as runner:
        assert_command_cleans_path(runner, paths.render_path, 'render')


def test_render_command_accepts_facts_as_cli_flags():
    with project_runner() as runner:
        runner.run('render --fact=cow_color:cherry')
        assert in_file('How now, cherry cow?')


def test_build_command_accepts_facts_as_cli_flags():
    with project_runner() as runner:
        runner.run('build --fact=cow_color:cinnabar')
        assert in_file('How now, cinnabar cow?')


def test_clean_command_removes_assets_with_clean_assets_flag():
    with project_runner() as runner:
        assert_command_cleans_path(runner, paths.assets_path, 'clean --clean-assets')


def test_build_command_removes_assets_with_clean_assets_flag():
    with project_runner() as runner:
        assert_command_cleans_path(runner, paths.assets_path, 'build --clean-assets')


def test_acquire_command_acquires_default_assets():
    with project_runner() as runner:
        assert command_acquires_asset(runner, 'acquire', 'default.tar.gz')


def test_acquire_command_does_not_acquire_non_default_assets():
    with project_runner() as runner:
        assert not command_acquires_asset(runner, 'acquire', 'special.tar.gz')


def test_acquire_command_acquires_assets_specified_by_asset_set_flag():
    with project_runner() as runner:
        assert command_acquires_asset(runner, 'acquire --asset-set=special', 'special.tar.gz')


def test_store_fact_flags_assigns_facts_in_config():
    args = (
        'key:minor',
        'tempo:adagio',
        'time_signature:3:4'  # <- Extra colon. Will it work?
    )
    store_fact_flags(args)
    assert pyconfig.get('cli.flags.fact')['key'] == 'minor'
    assert pyconfig.get('cli.flags.fact')['tempo'] == 'adagio'
    assert pyconfig.get('cli.flags.fact')['time_signature'] == '3:4'
